"""
CS50:          https://cs50.harvard.edu/weeks
Problem set 7: https://docs.cs50.net/2017/x/psets/7/pset7.html
Problem 1:     https://docs.cs50.net/problems/finance/finance.html

This program implements a mock-up website fro stocks trading.
"""

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session
# from passlib.apps import custom_app_context as pwd_context
from passlib.hash import scram as pwd_context
from tempfile import mkdtemp
from time import gmtime, strftime

from helpers import *

# configure application
app = Flask(__name__)

# ensure responses aren't cached
if app.config["DEBUG"]:
    @app.after_request
    def after_request(response):
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Expires"] = 0
        response.headers["Pragma"] = "no-cache"
        return response

# custom filter
app.jinja_env.filters["usd"] = usd

# configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

@app.route("/")
@login_required
def index():

    # get user portfolio
    user_dict = db.execute('SELECT quote, shares FROM portfolio WHERE user_id=:user_id', user_id=session['user_id'])

    # estimate it's value
    total_value = 0
    if len(user_dict) != 0:
        for item in user_dict:

            # complicated get current price to make sure yahoo responded
            price_data = None
            while price_data == None:
                price_data = lookup(item['quote'])
            current_price = price_data['price']

            # calculate share value etc.
            item['price'] = current_price
            item['value'] = round(current_price * item['shares'], 2)
            total_value += item['value']

    # get total portfolio value
    cash_balance = db.execute('SELECT cash FROM users WHERE id=:user_id', user_id=session['user_id'])[0]['cash']
    total_value += cash_balance

    # render
    return render_template('index.html', user_dict=user_dict, cash_balance=round(cash_balance, 2), total_value=usd(total_value))

@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock."""

    # if submitting data
    if request.method == 'POST':

        # check if correct input
        if not request.form.get('quote') or not request.form.get('shares') or int(request.form.get('shares')) <= 0:
            return apology('Must provide quote and number of shares to buy')

        # check if quote exist
        quote_dict = lookup(request.form.get('quote'))
        if not quote_dict:
            return apology('Invalid quote')

        # check if can afford
        stock = request.form.get('quote')
        shares = float(request.form.get('shares'))
        rows = db.execute('SELECT * FROM users WHERE id = :id', id=session['user_id'])
        if rows[0]["cash"] < quote_dict['price'] * shares:
            return apology('Cant afford')

        # buy and update user's cash
        db.execute('UPDATE users SET cash = cash - :cost WHERE id = :id',
                   cost=quote_dict['price']*shares, id=session['user_id'])

        # update portfolio
        has_stock_already = db.execute('SELECT quote FROM portfolio WHERE user_id=:user_id AND quote=:quote',
                                       user_id=session['user_id'], quote=stock)
        if not has_stock_already:
            db.execute('INSERT INTO portfolio (user_id, quote, shares) VALUES(:user_id, :quote, :shares)',
                       user_id=session['user_id'], quote=stock, shares=shares)
        else:
            db.execute('UPDATE portfolio SET shares=shares+:shares WHERE user_id=:user_id AND quote=:quote',
                       shares=shares, user_id=session["user_id"], quote=stock)

        # update history
        db.execute('INSERT INTO history (user_id, quote, shares, buy_or_sell, time, price) \
                   VALUES(:user_id, :quote, :shares, :buy_or_sell, :time, :price)',
                   user_id=session['user_id'], quote=stock, shares=shares, buy_or_sell=1,
                   time=strftime("%Y-%m-%d %H:%M:%S", gmtime()), price=quote_dict['price'])

        return index()

    else:
        return render_template('buy.html')

@app.route("/history")
@login_required
def history():
    """Show history of transactions."""

    user_dict = db.execute('SELECT * FROM history WHERE user_id=:user_id ORDER BY time', user_id=session['user_id'])

    return render_template('history.html', user_dict=user_dict)

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in."""

    # forget any user_id
    session.clear()

    # if user reached route via POST (as by submitting a form via POST)
    if request.method == 'POST':

        # ensure username was submitted
        if not request.form.get('username'):
            return apology('must provide username')

        # ensure password was submitted
        elif not request.form.get('password'):
            return apology('must provide password')

        # query database for username
        rows = db.execute('SELECT * FROM users WHERE username = :username', username=request.form.get('username'))

        # ensure username exists and password is correct
        if len(rows) != 1 or not pwd_context.verify(request.form.get('password'), rows[0]['hash']):
            return apology('invalid username and/or password')

        # remember which user has logged in
        session['user_id'] = rows[0]['id']

        # redirect user to home page
        return index()

    # else if user reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template('login.html')

@app.route("/logout")
def logout():
    """Log user out."""

    # forget any user_id
    session.clear()

    # redirect user to login form
    return redirect(url_for('login'))

@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():

    # if submitting data
    if request.method == 'POST':

        # check if quote is provided
        if not request.form.get('quote'):
            return apology('No quote provided!')

        # check for provided quote and display
        quote_dict = lookup(request.form.get('quote'))
        if quote_dict != None:
            return render_template('quote_display.html', quote_dict=quote_dict)
        else:
            return apology('Cound not find this quote!')

    # if accessing page
    else:
        return render_template('quote.html')


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user."""

    # if submitting data
    if request.method == 'POST':

        # check if username and 2x passwords are provided
        if not request.form.get('username') or not request.form.get('password') or not request.form.get('confirm_password'):
            return apology('must provide username, 2x passwords')

        # # check if passwords match
        if request.form.get('password') != request.form.get('confirm_password'):
            return apology('Passwords do not match!')

        # # create new user in db
        rows = db.execute('INSERT INTO users (username, hash) VALUES(:username, :hash)',
                          username=request.form.get('username'), hash=pwd_context.hash(request.form.get('password')))

        # # check if user was created successfully
        if not rows:
            return apology('Username already taken!')

        # # login user using its primary key (id)
        session['user_id'] = rows

        # return
        return render_template('index.html')

    # if accessing page
    else:
        return render_template('register.html')


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock."""

    if request.method == 'POST':

        # check if inputs are provided
        if not request.form.get('quote') or not request.form.get('shares'):
            return apology('Provide a quote and shares to sell!')

        # get user's portfolio
        rows = db.execute('SELECT quote, shares FROM portfolio WHERE user_id=:user_id', user_id=session['user_id'])

        # estimate transation value
        price = float(lookup(request.form.get('quote'))['price'])
        transaction_value = price * float(request.form.get('shares'))

        # sell
        for item in rows:
            if item['quote'] == request.form.get('quote') and int(item['shares']) >= int(request.form.get('shares')):

                # update user cash
                db.execute('UPDATE users SET cash=cash+:transaction_value WHERE id=:user_id',
                           transaction_value=transaction_value, user_id=session['user_id'])

                # udpate portfolio
                db.execute('UPDATE portfolio SET shares=shares-:shares WHERE user_id=:user_id AND quote=:quote',
                           shares=request.form.get('shares'), user_id=session['user_id'], quote=request.form.get('quote'))

                # new history instance
                db.execute('INSERT INTO history (user_id, quote, shares, buy_or_sell, time, price)\
                           VALUES(:user_id, :quote, :shares, :buy_or_sell, :time, :price)',
                           user_id=session["user_id"], quote=request.form.get('quote'), shares=request.form.get('shares'),
                           buy_or_sell=-1, time=strftime("%Y-%m-%d %H:%M:%S", gmtime()), price=price)

                return index()

            else:
                apology("You don't have this share or that many particular shares!")

    # if accessing page
    else:
        return render_template('sell.html')

@app.route("/change", methods=["GET", "POST"])
def change():

    if request.method == 'POST':

        # check if all data is filled
        if not request.form.get('username') or \
        not request.form.get('password') or \
        not request.form.get('new_password') or \
        not request.form.get('confirm_new_password'):
            return apology('You forgot to fill smthng!')

        # check if user exist
        if not db.execute('SELECT hash FROM users WHERE username=:user', user=request.form.get('username')):
            return apology('Wrong password (current) or no such user!') # not saying 'no such user' on purpose

        # check if current passwords match
        if not pwd_context.verify(request.form.get('password'),
        db.execute('SELECT hash FROM users WHERE username=:user', user=request.form.get('username'))[0]['hash']):
            return apology('Wrong password (current) or no such user!')

        # check if new passwords match
        if request.form.get('new_password') != request.form.get('confirm_new_password'):
            return apology('New passwords do not match!')

        # change password
        new_hash = pwd_context.hash(request.form.get('new_password'))
        db.execute('UPDATE users SET hash=:new_hash WHERE username=:user',
                   new_hash=new_hash, user=request.form.get('username'))

        return render_template('login.html')

    else:
        return render_template('change.html')