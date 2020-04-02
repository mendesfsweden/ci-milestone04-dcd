#!/usr/bin/env python3
from flask import Blueprint, jsonify, render_template, request
from app import mongo
from app.utils import recipes_collection, visitors_collection
import requests


# --------------------- #
#    Flask Blueprint    #
# --------------------- #
main = Blueprint("main", __name__)


# ---------------- #
#    APP ROUTES    #
# ---------------- #

# ----- HOME ----- #
@main.route("/")
def home():
    """ Home page with sample of 8 random recipes in a Carousel. """
    carousel = (
        [recipe for recipe in recipes_collection.aggregate([
            {"$sample": {"size": 8}}])])

    """ Add site user to list of visitors. """
    response = requests.get("https://ipapi.co/json/").json()  # get ip data
    if response:
        ip = response["ip"]
        # check if existing ip visitor already exists
        if visitors_collection.count_documents({"ip": ip}, limit=1) == 0:
            submit = {
                "ip": ip,
                "city": response["city"],
                "region": response["region"],
                "country": response["country_name"],
                "latitude": response["latitude"],
                "longitude": response["longitude"],
                "timezone": response["timezone"],
                "utc_offset": response["utc_offset"]
            }
            visitors_collection.insert_one(submit)

    return render_template("index.html", carousel=carousel)
