from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
import datetime
import yfinance as yf
import os

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/stockportfolio', methods = ['POST'])
def generatePortfolio():
    s1 = request.form['strategy1']
    s2 = request.form['strategy2']
    value = request.form['value']
    return render_template('stockportfolio.html', strategy1 = s1, strategy2 = s2, value = value) 