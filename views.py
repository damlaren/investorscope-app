from app import app
from flask import render_template, request, redirect, url_for
from models import Stock, User, UsernameError, PasswordError
from forms import LoginForm

# Home screen.
@app.route("/home.html")
@app.route("/")
def home():
    return render_template("home.html")

# Search form submission from home.
@app.route("/submit_search", methods=["POST"])
def submit_search():
    ticker = request.form["search_string"]
    return redirect(url_for("stock", ticker=ticker))

# Q&A stock recommender.
@app.route("/question.html")
def question():
    return render_template("question.html")

# Stock data page.
@app.route("/stock.html")
def stock():
    ticker = request.args.get("ticker", "AAPL")

    # Find the stock.
    stock = Stock.get_stock_from_db(ticker)
    
    return render_template("stock.html", ticker=stock.ticker, name=stock.name,
                           latest_price=stock.latest_price)

# Login page. TODO: POST to do the login
@app.route("/login.html", methods=["GET", "POST"])
def login():
    form = LoginForm(request.form)
    
    #TODO: check session if user already logged in
    if request.method == "POST" and form.validate():
        try:
            User.check_user_password(form.username.data,
                                     form.password.data)
            return redirect(url_for("home"))
        except UsernameError:
            #TODO: what is "the right way" to add new errors?
            form.username.errors.append("Unrecognized username.")
        except PasswordError:
            form.password.errors.append("Incorrect password.")
        
    #TODO: error messages for missing username, pword        
    return render_template("login.html", form=form)
