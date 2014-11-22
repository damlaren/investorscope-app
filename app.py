import os
from flask import Flask, render_template, request, redirect, url_for
from flask.ext.mongoengine import MongoEngine

# ------------------------------
# Setting up the program.
# ------------------------------
app = Flask(__name__)
app.config['MONGODB_SETTINGS'] = {
	'db': 'investorscope',
	'host': 'ds053300.mongolab.com',
	'port': 53300,
	'username': 'dkhavari',
	'password': 'invest'
}
db = MongoEngine(app)

import models # must be after db created

# ------------------------------
# TEST: Ensure functional mongo
# ------------------------------

# class Person(db.Document):
# 	name = db.StringField()
# 	meta = {
# 		'collection': 'users'
# 	}

# collection = Person._get_collection()
# collection.insert({'name': 'david'})

# ------------------------------
# END TEST: Ensure func. mongo
# ------------------------------

@app.route("/home.html")
@app.route("/")
def home():
    return render_template("home.html")

# search form submission from main page.
# this would be better as an auto-complete function.
@app.route("/submit_search", methods=["POST"])
def submit_search():
    ticker = request.form["search_string"]
    return redirect(url_for("stock", ticker=ticker))

@app.route("/question.html")
def question():
    return render_template("question.html")

@app.route("/stock.html")
def stock():
    ticker = request.args.get("ticker","AAPL").upper()
    return render_template("stock.html", ticker=ticker)
