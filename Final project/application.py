from flask import Flask, request, render_template, jsonify
from helpers import check_users_list, get_tweets, clean_tweets, get_sentiment, parse_all_data, get_chart


# initiate app
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/sample')
def sample():

    # request arguments
    user_list = request.args.get('user_list')

    # check for args
    if not user_list:
        return render_template('404.html')

    # reshape arguments
    user_list = user_list.split(';')

    # check if users exist
    user_info = check_users_list(user_list)
    if not user_info:
        return jsonify(['No such user: {}'. format(user_info)])

    # get tweets and clean tweet text
    tweets_data = get_tweets(user_list)
    tweets_data = clean_tweets(tweets_data)

    # get sentiment
    tweets_sentiment = get_sentiment(tweets_data)

    # parse data
    tweets_data_sentiment = parse_all_data(tweets_data, tweets_sentiment)

    # create new list to iterate over with zip
    chart = get_chart(tweets_data_sentiment)

    return render_template('sample.html', chart=chart)
