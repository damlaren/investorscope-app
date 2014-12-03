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
    cur_price = db.StringField(db_field = "cur-price")
    cap = db.StringField() # market cap
    pe = db.StringField() # price/earnings ratio
    eps = db.StringField() # earnings per share
    dividends = db.StringField()
    one_year_est = db.FloatField()
    beta = db.StringField()
    sustainability = db.StringField()
    # Add more as necessary.

    recommended_tickers = ["ABX", "AFSD", "BBL", "BDN", "CAJ",
                           "CHA", "COF", "DSW", "EMN", "EVGN",
                           "FGP", "GD", "GE", "HHC", "IGI",
                           "JMI", "KMX", "LQ", "QIHU", "RBS"]

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
            return -1 # Create a way of propagating the error here.
        return sub_collection[0]

    # Get list of stocks that aren't all screwed up.
    @staticmethod
    def get_valid_stocks():
        return Stock.objects(cur_price__ne="Inc.").filter(cur_price__ne="L.P.")

    # Get <n> stocks with no specified sort order, just alphabetical.
    # But filter 
    @staticmethod
    def get_stocks(n, ascending):
        order_str = "ticker" if ascending else "-ticker"
        return Stock.get_valid_stocks().order_by(order_str)[:n]

    # Get <n> stocks sorted by pe ratio
    @staticmethod
    def get_stocks_sorted_by_pe(n, ascending):
        order_str = "pe" if ascending else "-pe"
        return Stock.get_valid_stocks().filter(pe__ne="N/A").order_by(order_str)[:n]

    # Get <n> stocks sorted by price
    # TODO: there's more than a few stocks with price = 0.
    # Time to invest in MOOG?
    @staticmethod
    def get_stocks_sorted_by_price(n, ascending):
        order_str = "cur_price" if ascending else "-cur_price"
        return Stock.get_valid_stocks().filter(cur_price__ne=0).order_by(order_str)[:n]

    # Get <n> stocks sorted by market cap
    # TODO: this doesn't work. market cap is a string, and annoying to convert.
    @staticmethod
    def get_stocks_sorted_by_cap(n, ascending):
        order_str = "cap" if ascending else "-cap"
        return Stock.get_valid_stocks().order_by(order_str)[:n]

    # Get <n> stocks sorted by risk (beta)
    # High beta = high risk
    @staticmethod
    def get_stocks_sorted_by_risk(n, ascending):
        order_str = "beta" if ascending else "-beta"
        return Stock.get_valid_stocks().filter(beta__ne="N/A").order_by(order_str)[:n]

    # Get <n> stocks sorted by sustainability rating.
    @staticmethod
    def get_stocks_sorted_by_sustainability(n, ascending):
        order_str = "sustainability" if ascending else "-sustainability"
        return Stock.get_valid_stocks().order_by(order_str)[:n]

    # Get all stock tickers, no limits
    @staticmethod
    def get_all_tickers():
        all_tickers = Stock.objects.distinct('ticker')
        return all_tickers

    # Get historic stock data for last 7 days.
    # - ticker_string: Stock to retrive data for.
    # - num_days: # of days for which to retrieve data
    # returns series of prices from last week (rounded to 2 decimal places),
    #         as a map from datetime.date -> price ($)
    @staticmethod
    def get_time_series(ticker_string, num_days):
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
        for i in range(0, num_days):
            # go up or down by some percent each day
            curr_day -= dt
            delta = (float(randrange(0, brackets)) / brackets - 0.5) * maxchange
            percent += delta
            if percent < 0:
                percent = 0
            price = round(percent * base_price, 2)
            series[curr_day] = price
        return series

    # Get a list of stocks from our state of the art recommendation engine.
    @staticmethod
    def get_recommendations():
        return Stock.objects(ticker__in=Stock.recommended_tickers)

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


class Question(db.DynamicDocument):

    meta = {
        "collection": "questions"
    }

    prompt = db.StringField()
    choices = [db.StringField()]

    def __repr__(self):
        return prompt
