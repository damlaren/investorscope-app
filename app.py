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

# add a super-secret key so sessions work
#app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

# ------------------------------
# TEST: Ensure functional mongo
# ------------------------------

from models import Stock
collection = Stock._get_collection()
collection.insert({'ticker': 'AAPL', 'name': 'Apple Inc.', 'latest_price': 120})

from models import User
collection = User._get_collection()
collection.insert({'username': 'x', 'password': 'x'})

# ------------------------------
# END TEST: Ensure func. mongo
# ------------------------------

import views # All the routing is in here.
