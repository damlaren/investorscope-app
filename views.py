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
    
    return render_template("stock.html", ticker = stock.ticker,
                           name = stock.name, latest_price = stock.cur_price,
                           pe_ratio = stock.pe, market_cap = stock.cap,
                           dividends = stock.dividends)

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
