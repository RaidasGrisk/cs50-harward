"""
CS50:          https://cs50.harvard.edu/weeks
Problem set 8: https://docs.cs50.net/2017/x/psets/8/pset8.html
Problem 1:     https://docs.cs50.net/problems/mashup/mashup.html#typeahead-js

This program implements a website that collects news based on current location on a map
using google maps API (for locations) and google news feed (for news, obviously).
"""

import os
import re
from flask import Flask, jsonify, render_template, request, url_for
from flask_jsglue import JSGlue

from cs50 import SQL
from helpers import lookup

# configure application
app = Flask(__name__)
JSGlue(app)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///mashup.db")

@app.route("/")
def index():
    """Render map."""
    if not os.environ.get("API_KEY"):
        raise RuntimeError("API_KEY not set")
    return render_template("index.html", key=os.environ.get("API_KEY"))

@app.route("/articles")
def articles():
    """Look up articles for geo."""

    # ensure parameters are present
    geo = request.args.get("geo")
    if not geo:
        raise RuntimeError("missing geo")

    # loop up for articles
    articles = lookup(geo)

    # ensure list contains no more than 5 articles
    if len(articles) > 5:
        articles = articles[0:5]

    # return a json object of articles
    return jsonify(articles)

@app.route("/search")
def search():
    """Search for places that match query."""

    # ensure parameters are present
    q = request.args.get("q")
    if not q:
        raise RuntimeError("missing q")

    # get db data
    # https://www.w3schools.com/sql/sql_like.asp
    q = q + "%"
    geo_data = db.execute("SELECT * FROM places WHERE \
                                                  postal_code LIKE :q OR \
                                                  admin_name1 LIKE :q OR \
                                                  place_name  LIKE :q",
                                                  q=q)

    # ensure list contains no more than 5 articles
    if len(geo_data) > 10:
        geo_data = geo_data[0:10]

    # return a json object of geo data
    return jsonify(geo_data)

@app.route("/update")
def update():
    """Find up to 10 places within view."""

    # ensure parameters are present
    if not request.args.get("sw"):
        raise RuntimeError("missing sw")
    if not request.args.get("ne"):
        raise RuntimeError("missing ne")

    # ensure parameters are in lat,lng format
    if not re.search("^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$", request.args.get("sw")):
        raise RuntimeError("invalid sw")
    if not re.search("^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$", request.args.get("ne")):
        raise RuntimeError("invalid ne")

    # explode southwest corner into two variables
    (sw_lat, sw_lng) = [float(s) for s in request.args.get("sw").split(",")]

    # explode northeast corner into two variables
    (ne_lat, ne_lng) = [float(s) for s in request.args.get("ne").split(",")]

    # find 10 cities within view, pseudorandomly chosen if more within view
    if (sw_lng <= ne_lng):

        # doesn't cross the antimeridian
        rows = db.execute("""SELECT * FROM places
            WHERE :sw_lat <= latitude AND latitude <= :ne_lat AND (:sw_lng <= longitude AND longitude <= :ne_lng)
            GROUP BY country_code, place_name, admin_code1
            ORDER BY RANDOM()
            LIMIT 10""",
            sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)

    else:

        # crosses the antimeridian
        rows = db.execute("""SELECT * FROM places
            WHERE :sw_lat <= latitude AND latitude <= :ne_lat AND (:sw_lng <= longitude OR longitude <= :ne_lng)
            GROUP BY country_code, place_name, admin_code1
            ORDER BY RANDOM()
            LIMIT 10""",
            sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)

    # output places as JSON
    return jsonify(rows)
