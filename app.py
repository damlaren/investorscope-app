import os
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/home.html')
@app.route('/')
def home():
    return render_template('home.html')

@app.route('/question.html')
def question():
    return render_template('question.html')

@app.route('/stock.html')
def stock():
    return render_template('stock.html')
