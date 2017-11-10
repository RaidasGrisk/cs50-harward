"""
CS50:          https://cs50.harvard.edu/weeks
Problem set 6: https://docs.cs50.net/2017/x/psets/6/pset6.html
Problem 5:     https://docs.cs50.net/problems/sentiments/sentiments.html

In this file and object named Analizer is defined. This object is used to estimate sentiment value of a given text.
"""

class Analyzer():
    """Implements sentiment analysis."""

    def __init__(self, positives, negatives):
        """Initialize Analyzer."""

        # prepare words_positive: store words in a set
        self.words_positives = set()
        positives_txt = open(positives, 'r')
        for line in positives_txt:
            if line[0] != ';':
                self.words_positives.add(line.strip('\n'))

        # prepare words_negative: store words in a set
        self.words_negatives = set()
        negatives_txt = open(negatives, 'r')
        for line in negatives_txt:
            if line[0] != ';':
                self.words_negatives.add(line.strip('\n'))

    def analyze(self, text):
        """Analyze text for sentiment, returning its score."""

        # prepare text: lower case and store words in a list
        words_text = text.lower().split()

        # estimate sentiment
        sentiment = 0
        for word in words_text:
            if word in self.words_positives:
                sentiment += 1
            elif word in self.words_negatives:
                sentiment -= 1

        # return
        return sentiment
