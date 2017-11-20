"""
This is the file where most of the utils functions are stored.
"""

from twython import Twython
from encoder import Model
from datetime import datetime, timedelta
import plotly
import plotly.graph_objs as go
import numpy as np

# https://twython.readthedocs.io/en/latest/usage/starting_out.html#beginning
# these are private, do not steal them!
APP_KEY = 'uK6XbhFSAUVt1mMQ2YRIPdvc2'
APP_SECRET = 'Jprdcz665adbP7TwQu1afic7F6VtDla8yF4Av3DLF2lzde4XR4'
ACCESS_TOKEN = 'AAAAAAAAAAAAAAAAAAAAAHro3AAAAAAADdTBFEsDUoH5xP01uS2oZYxQjhI%3DFSay2sXNRwqOqcroOgh0dvjVn5B6R0DAPr1RmlTjb200R5CGCS'

# global variables
twitter = Twython(APP_KEY, access_token=ACCESS_TOKEN)
model = Model()


def check_users_list(user_list):
    """Checks if user accounts are available. Returns True if available, user's name if not"""

    for user in user_list:
        try:
            twitter.lookup_user(screen_name=user)
        except:
            return user
    return True


def get_tweets(user_list, count=5):
    """Get users tweets and return structured dictionary"""

    """
    check tweet_mode for full tweets

    """

    # empty dictionary to store data
    data = {}

    # get user's data
    for user in user_list:
        tweets = twitter.get_user_timeline(screen_name=user, count=count)
        data['{}'.format(user)] = []

        # structure user's data
        for tweet in tweets:
            data['{}'.format(user)].append(
                [tweet['text'], tweet['created_at'], tweet['favorite_count'] + tweet['retweet_count']])

    return data


def clean_tweets(tweets_data):
    """Cleans text. Removes https, @names, etc."""

    for user in tweets_data:
        for tweet in tweets_data['{}'.format(user)]:
            clean_text = ''
            raw_text = tweet[0].split()
            for word in raw_text:
                if word[0:5] != 'https' and word[0] != '@' and word != 'RT' and word[0] != '#':
                    clean_text += word + ' '
            tweet[0] = clean_text

    return tweets_data


def get_sentiment(tweets_data):
    """Estimate sentiment value using OpenAI's sentiment neuron"""

    # prepare tweets_data to feed into nn
    input = []
    for user in tweets_data:
        for tweet in tweets_data['{}'.format(user)]:
            input.append(tweet[0])

    # get sentiment
    tweet_features = model.transform(input)
    sentiment = list(tweet_features[:, 2388])

    # cast to float and round
    sentiment_t = [round(float(i), 4) for i in sentiment]

    return sentiment_t


def parse_all_data(tweets_data, tweets_sentiment):
    """Parse all the data into dictionary"""

    # append sentiment to existing data
    c = 0
    for user in tweets_data:
        for tweet in tweets_data['{}'.format(user)]:
            tweet.append(tweets_sentiment[c])
            c += 1

    return tweets_data


def get_time_series_data(tweets_data, granularity=1):
    """Form time-series data"""

    last_time, first_time = datetime(2000, 1, 1, 1, 1, 1), datetime(2100, 1, 1, 1, 1, 1)

    # format datetime, get times of first and last tweets, count tweets
    for user in tweets_data:
        for tweet in tweets_data['{}'.format(user)]:

            # Else: time.strftime('%Y-%m-%d %H:%M:%S', time.strptime(tweet[1], '%a %b %d %H:%M:%S +0000 %Y'))
            # https://stackoverflow.com/questions/18711398/converting-twitters-date-format-to-datetime-in-python
            tweet[1] = datetime.strptime(tweet[1], '%a %b %d %H:%M:%S %z %Y').replace(tzinfo=None)

            # get time span of tweets
            if tweet[1] > last_time:
                last_time = tweet[1]
            if tweet[1] < first_time:
                first_time = tweet[1]

    # create time scale for time-series
    time_series = [first_time.replace(second=0, minute=0)]
    while last_time > time_series[-1]:
        time_series.append(time_series[-1] + timedelta(hours=1))

    # create final output
    tweets_data_ordered = [[[time_series[i]]] for i in range(len(time_series)-1)]
    for user in tweets_data:
        for tweet in tweets_data['{}'.format(user)]:
            for t in range(len(time_series)-1):
                if time_series[t] < tweet[1] < time_series[t+1]:
                    tweets_data_ordered[t].append(
                        [{'user': user, 'text': tweet[0], 'time': tweet[1], 'likes': tweet[2], 'sentiment': tweet[3]}])

    return tweets_data_ordered


def get_chart(tweets_data_sentiment):

    """Form a sample chart including sentiment, likes (and shares).
    Not a time-series. Used for sample plot only"""

    # create new list to iterate over with zip
    tweets_data_sentiment_for_chart = []
    for user in tweets_data_sentiment:
        tweets_data_sentiment_for_chart.append(tweets_data_sentiment['{}'.format(user)])

    # save likes and sentiment data
    likes, sentiment = [], []
    for item in zip(*tweets_data_sentiment_for_chart):
        c = 0
        for element in zip(*item):
            if c == 2:
                likes.append(element)
            if c == 3:
                sentiment.append(element)
            c += 1

    # estimate sentiment
    sentiment_values = np.sum(sentiment * (likes / np.sum(likes, axis=1, keepdims=True)), axis=1)
    likes = np.sum(likes, axis=1)

    # create chart
    chart = [go.Scatter(x=[i for i in range(len(likes))], y=sentiment_values)]

    return plotly.offline.plot(chart, output_type='div', show_link=False, link_text=False)
