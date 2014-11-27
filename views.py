from app import app
from flask import render_template, request, redirect, url_for
from models import Stock, User, UsernameError, PasswordError
from forms import LoginForm
from account import user_is_logged_in, user_log_in, user_log_out

# Home screen.
@app.route("/home.html")
@app.route("/")
def home():
    if not user_is_logged_in():
        return redirect(url_for("login"))
    tickers = Stock.get_all_tickers()
    stocks = Stock.get_stocks(20)
    return render_template("home.html", tickers = tickers, stocks = stocks)

# Search form submission from home.
@app.route("/submit_search", methods=["POST"])
def submit_search():
    ticker = request.form["search_string"]
    return redirect(url_for("stock", ticker = ticker))

# Q&A stock recommender.
@app.route("/question.html")
def question():
    if not user_is_logged_in():
        return redirect(url_for("login"))
    return render_template("question.html")

# Stock data page.
@app.route("/stock.html")
def stock():
    if not user_is_logged_in():
        return redirect(url_for("login"))
    ticker = request.args.get("ticker", "AAPL") # default is AAPL

    # Find the stock.
    stock = Stock.get_stock_from_db(ticker)

    # Get the prices with corresponding dates.
    # Produce formatted date strings to paste into HTML.
    price_time_series = Stock.get_time_series(ticker)
    price_dates = price_time_series.keys()
    price_dates.sort()
    price_dates_str = []
    price_values = []
    for curr_date in price_dates:
        price_values.append(price_time_series[curr_date])
        price_dates_str.append(curr_date.strftime("%m-%d"))

    # Compute price change now-- consistent with time series data!
    price_change = price_values[-1] - price_values[-2]

    return render_template("stock.html", ticker = stock.ticker,
                           name = stock.name, latest_price = stock.cur_price,
                           pe_ratio = stock.pe, market_cap = stock.cap,
                           dividends = stock.dividends,
                           price_change = price_change,
                           price_series_dates = price_dates_str,
                           price_series_values = price_values)

# Login page.
@app.route("/login.html", methods=["GET", "POST"])
def login():
    if user_is_logged_in():
        return redirect(url_for("home"))

    form = LoginForm(request.form)
    
    if request.method == "POST" and form.validate():
        try:
            User.check_user_password(form.username.data,
                                     form.password.data)

            # password is good (no exceptions thrown)
            # TODO: logout button somewhere
            user_log_in()
            
            return redirect(url_for("home"))
        except UsernameError:
            #TODO: what is "the right way" to add new errors?
            form.username.errors.append("Unrecognized username.")
        except PasswordError:
            form.password.errors.append("Incorrect password.")
        
    return render_template("login.html", form=form)
