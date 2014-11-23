from app import db

class Stock(db.DynamicDocument):

    # Meta variables.
    meta = {
        "collection": "stocks"
    }

    # Model variables.
    ticker = db.StringField()
    name = db.StringField()
    latest_price = db.FloatField()
    # TODO: sustainability, freshness, whatever

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
            return Stock()
        return sub_collection[0]

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
