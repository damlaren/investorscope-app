from app import app
from flask import render_template, request, redirect, url_for
from models import Stock, User, UsernameError, PasswordError
from forms import LoginForm
import account

# Home screen.
@app.route("/home.html")
@app.route("/")
def home():
    N_STOCKS = 20 # number of stocks to retrieve
    if not account.user_is_logged_in():
        return redirect(url_for("login"))

    # Get all stock tickers
    tickers = Stock.get_all_tickers()

    # Get default sorting metric and order 
    order = None
    metric = request.args.get("metric", "alpha")
    order_arg = request.args.get("order", "lowhigh")
    if order_arg == "lowhigh":
        order = True
    elif order_arg == "highlow":
        order = False

    # Get sorted stocks
    stocks = None
    if metric == "alpha":
        stocks = Stock.get_stocks(N_STOCKS, order)
    elif metric == "price":
        stocks = Stock.get_stocks_sorted_by_price(N_STOCKS, order)
    elif metric == "pe":
        stocks = Stock.get_stocks_sorted_by_pe(N_STOCKS, order)
    elif metric == "risk":
        stocks = Stock.get_stocks_sorted_by_risk(N_STOCKS, order)
    elif metric == "recs":
        stocks = Stock.get_recommendations()

    return render_template("home.html", tickers = tickers, stocks = stocks,
                           metric = metric, order = order,
                           has_recs = account.user_has_recommendations())

# Search form submission from home.
@app.route("/submit_search", methods=["POST"])
def submit_search():
    ticker = request.form["search_string"]
    return redirect(url_for("stock", ticker = ticker))

# Stock data page.
@app.route("/stock.html")
def stock():
    if not account.user_is_logged_in():
        return redirect(url_for("login"))
    ticker = request.args.get("ticker", "AAPL") # TODO: no ticker is error...

    # Find the stock.
    stock = Stock.get_stock_from_db(ticker)

    # Check for errors.
    if stock == -1:
        N_STOCKS = 20 # number of stocks to retrieve
        tickers = Stock.get_all_tickers()
        stocks = Stock.get_stocks(N_STOCKS, True) # default: list of stocks by alpha order

        return render_template("home.html",
                               error="No ticker matching that name could be found.",
                               tickers = tickers, stocks = stocks,
                               metric = "alpha", order = True,
                               has_recs = account.user_has_recommendations())

    # Get the prices with corresponding dates.
    # Produce formatted date strings to paste into HTML.
    price_time_series = Stock.get_time_series(ticker, 7)
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
                           beta = stock.beta,
                           price_change = price_change,
                           price_series_dates = price_dates_str,
                           price_series_values = price_values)

# Login page.
@app.route("/login.html", methods=["GET", "POST"])
def login():
    if account.user_is_logged_in():
        return redirect(url_for("home"))

    form = LoginForm(request.form)
    
    if request.method == "POST" and form.validate():
        try:
            User.check_user_password(form.username.data,
                                     form.password.data)

            # password is good (no exceptions thrown)
            account.user_log_in()
            
            return redirect(url_for("home"))
        except UsernameError:
            #TODO: what is "the right way" to add new errors?
            form.username.errors.append("Unrecognized username.")
        except PasswordError:
            form.password.errors.append("Incorrect password.")
        
    return render_template("login.html", form=form)

# Logout route.
@app.route("/logout.html")
def logout():
    account.user_log_out()
    return redirect(url_for("login"))

# --------------------------------------------------
# Faked-up question and recommendation routing.
# --------------------------------------------------

# Question page one.
@app.route("/question.html")
def question():
    if not account.user_is_logged_in():
        return redirect(url_for("login"))
    return render_template("question.html")

# Question page two.
@app.route("/question-two.html")
def question_two():
    if not account.user_is_logged_in():
        return redirect(url_for("login"))
    return render_template("question-two.html")

# Question page three.
@app.route("/question-three.html")
def question_three():
    if not account.user_is_logged_in():
        return redirect(url_for("login"))
    return render_template("question-three.html")

# Recommended page.
@app.route("/recommended.html")
def recommend():
    if not account.user_is_logged_in():
        return redirect(url_for("login"))

    # The user has now completed the recommendation process.
    account.user_store_recommendations()

    return redirect(url_for("home", metric = "recs", order = True))
