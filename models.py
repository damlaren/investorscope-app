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
    market_cap = db.StringField()
    price_earnings = db.FloatField()
    eps = db.FloatField()
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
            return Stock()
        return sub_collection[0]

    @staticmethod
    def get_all_tickers():
        all_tickers = Stock.objects.distinct('ticker')
        return all_tickers
