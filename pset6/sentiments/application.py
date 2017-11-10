"""
CS50:          https://cs50.harvard.edu/weeks
Problem set 6: https://docs.cs50.net/2017/x/psets/6/pset6.html
Problem 5:     https://docs.cs50.net/problems/sentiments/sentiments.html

This program runs a flask web server for categorizing someone's tweets and plitting tweet's sentiment pie chart.
"""

from flask import Flask, redirect, render_template, request, url_for

import os
import sys
import helpers
import analyzer
from analyzer import Analyzer

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/search")
def search():

    # validate screen_name
    screen_name = request.args.get("screen_name", "")
    if not screen_name:
        return redirect(url_for("index"))

    # get screen_name's tweets
    tweets = helpers.get_user_timeline(screen_name)
    if not tweets:
        return redirect(url_for("index"))

    # absolute paths to lists
    positives = os.path.join(sys.path[0], "positive-words.txt")
    negatives = os.path.join(sys.path[0], "negative-words.txt")

    # initialize analyzer
    tweet_analizer = analyzer.Analyzer(positives, negatives)

    # analyze each tweet's sentiment
    positive, negative, neutral = 0, 0, 0
    for tweet in tweets:
        sentiment = tweet_analizer.analyze(tweet)
        if sentiment < 0:
            negative += 1
        if sentiment > 0:
            positive += 1
        if sentiment == 0:
            neutral += 1

    # generate chart
    chart = helpers.chart(positive/len(tweets), negative/len(tweets), neutral/len(tweets))

    # render results
    return render_template("search.html", chart=chart, screen_name=screen_name)
