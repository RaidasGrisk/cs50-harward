from flask import Flask, request, render_template, jsonify
from helpers import check_users_list, get_tweets, clean_tweets, get_sentiment, \
                    parse_all_data, get_charts, get_time_series_data


# initiate app
app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/api_doc')
def api_doc():
    return render_template('api_doc.html')


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
    tweets_data = get_tweets(user_list, count=20)
    tweets_data = clean_tweets(tweets_data)

    # get sentiment
    tweets_sentiment = get_sentiment(tweets_data)

    # parse data
    tweets_data_sentiment = parse_all_data(tweets_data, tweets_sentiment)

    # get the two sample charts
    chart1, chart2 = get_charts(tweets_data_sentiment)

    return render_template('sample.html', chart1=chart1, chart2=chart2)


@app.route('/api', methods=['GET'])
def api():

    # request args
    user_list = request.args.get('user_list')
    count = request.args.get('count')
    TS = request.args.get('TS')

    # check for args
    if not user_list or not count or not TS:
        return jsonify('error')

    # reshape arguments
    user_list = user_list.split(';')

    # check if users exist
    user_info = check_users_list(user_list)
    if not user_info:
        return jsonify(['No such user: {}'. format(user_info)])

    # get tweets and clean tweet text
    tweets_data = get_tweets(user_list, count=count)
    tweets_data = clean_tweets(tweets_data)

    # get sentiment
    tweets_sentiment = get_sentiment(tweets_data)

    # parse data
    tweets_data_sentiment = parse_all_data(tweets_data, tweets_sentiment)

    # return
    if TS == "1":
        return jsonify(get_time_series_data(tweets_data_sentiment))
    else:
        return jsonify(tweets_data_sentiment)

