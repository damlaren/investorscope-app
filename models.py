from app import db
from random import seed, randrange
from datetime import date, timedelta

class Stock(db.DynamicDocument):

    # Meta variables.
    meta = {
        "collection": "stocks"
    }

    # Model variables.
    ticker = db.StringField()
    name = db.StringField()
    cur_price = db.StringField(db_field = "cur-price") # TODO: some are wrong
    cap = db.StringField() # market cap
    pe = db.FloatField() # price/earnings ratio
    eps = db.FloatField() # earnings per share
    dividends = db.StringField()
    one_year_est = db.FloatField()
    beta = db.FloatField()
    # Add more as necessary.

    def __repr__(self):
        return ticker

    # Get a stock from DB by ticker.
    # - ticker_string: Stock ticker symbol. Doesn't have to be uppercase.
    @staticmethod
    def get_stock_from_db(ticker_string):
        if not ticker_string:
            raise ValueError()
        sub_collection = Stock.objects(ticker=ticker_string.upper())
        results_size = len(sub_collection)
        if results_size == 0:
            return Stock() #TODO: not that useful...
        return sub_collection[0]

    # Get <n> stocks (for display on home page).
    # TODO: later, desirable to get stocks sorted by some metric
    @staticmethod
    def get_stocks(n):
        return Stock.objects[:n]

    # Get all stock tickers, no limits
    @staticmethod
    def get_all_tickers():
        all_tickers = Stock.objects.distinct('ticker')
        return all_tickers

    # Get historic stock data for last 7 days.
    # - ticker_string: Stock to retrive data for.
    # returns series of prices from last week (rounded to 2 decimal places),
    #         as a map from datetime.date -> price ($)
    @staticmethod
    def get_time_series(ticker_string):
        seed(ticker_string)
        stock = Stock.get_stock_from_db(ticker_string)
        base_price = stock.cur_price

        # work backwards for 6 more days
        percent = 1.0
        maxchange = 0.02 # max change (%) per day
        brackets = 100
        dt = timedelta(1) # 1-day time difference
        curr_day = date.today() # not bothering with TZ correction for prototype
        series = dict()
        series[curr_day] = base_price
        for i in range(0, 6):
            # go up or down by some percent each day
            curr_day -= dt
            delta = (float(randrange(0, brackets)) / brackets - 0.5) * maxchange
            percent += delta
            price = round(percent * base_price, 2)
            series[curr_day] = price
        return series

# Users, Usernames, Passwords
class UsernameError(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return "UsernameError"

class PasswordError(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return "PasswordError"

class User(db.DynamicDocument):
    meta = {
        "collection": "users"
    }

    username = db.StringField()
    password = db.StringField() #yayaya.

    def __repr__(self):
        return username

    # Get a User from DB by username.
    # - username: Username ...
    @staticmethod
    def get_user_from_db(username_string):
        if not username_string:
            raise ValueError()

        # Look for this user.
        sub_collection = User.objects(username=username_string)
        results_size = len(sub_collection)
        if results_size == 0:
            raise UsernameError()
        return sub_collection[0]

    # Check if password and username are correct. Raise exception if not.
    # - username: Username
    # - password: The password...
    @staticmethod
    def check_user_password(username, password):
        user = User.get_user_from_db(username) # throws UsernameError

        if not password:
            raise ValueError()

        # Check if password matches.
        if user.password != password:
            raise PasswordError()
