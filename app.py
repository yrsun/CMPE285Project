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

@app.route('/stockportfolio', methods = ['POST', "GET"])
def generatePortfolio():
    s1 = request.form['strategy1']
    s2 = request.form['strategy2']
    value = request.form['value']
    if not value and s1 == 'None' and s2 == 'None':
        error_messae = "No Inputs Detected"
        return render_template('error.html', error_message = error_messae)
    if not value or not value.isdecimal() or int(value) < 5000:
        error_messae = "Invalid Investment Value. Minimum Value is 5000$"
        return render_template('error.html', error_message = error_messae)
    if s1 == 'None' and s2 == 'None':
        error_messae = "No Strategy Selected"
        return render_template('error.html', error_message = error_messae)
    if s1 == s2:
        error_messae = "Invalid Inputs. Two Strategies Are Same"
        return render_template('error.html', error_message = error_messae)
    
    return render_template('stockportfolio.html', strategy1 = s1, strategy2 = s2, value = value) 