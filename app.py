from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
import yfinance as yf
import os
import io
import datetime as dt
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import base64
import numpy as np

app = Flask(__name__)
Bootstrap(app)

ethical = ['AAPL', 'MSFT', 'ADBE']
growth = ['AVGO', 'GPRO', 'NVDA']
index = ['FB', 'AMZN', 'HMC']
quality = ['JPM', 'WMT', 'BBY']
value = ['TSLA', 'TWTR', 'GOOG']

todays_date = dt.date.today()
last_n_days = 7
last_n_day = todays_date - dt.timedelta(days=last_n_days)

def getStock(s1, s2):
    stocks = []
    if s1 == 'Ethical Investing' or s2 == 'Ethical Investing':
        stocks += ethical
    if s1 == 'Growth Investing' or s2 == 'Growth Investing':
        stocks += growth
    if s1 == 'Index Investing' or s2 == 'Index Investing':
        stocks += index
    if s1 == 'Quality Investing' or s2 == 'Quality Investing':
        stocks += quality
    if s1 == 'Value Investing' or s2 == 'Value Investing':
        stocks += value
    stocks.sort()
    return stocks

def getStockInfo(stocks):
    stocksInfo = yf.download(" ".join(stocks), start=last_n_day, end=todays_date)
    return stocksInfo

def getStockClose(stocks, stocksInfo):
    stocks_list = []
    for s in range(len(stocks)):
        stock_list = []
        for d in range(last_n_days - 2):
            stock_list.append(stocksInfo.iloc[d][s+len(stocks)])
        stocks_list.append(stock_list)
    return stocks_list

def generateBarChart(stocks, stocksInfo):
    img = io.BytesIO()
    stocks_list = getStockClose(stocks, stocksInfo)
    X = np.arange(len(stocks_list[0]))
    fig = plt.figure()
    ax = fig.add_subplot()
    color = ['b', 'g', 'r', 'c', 'm', 'y']
    dis = 0.1 if len(stocks_list) > 3 else 0.2
    for i in range(len(stocks_list)):
        ax.bar(X+dis*i, stocks_list[i], color=color[i], width=dis)
    ax.legend(labels=stocks)
    ax.set_xticks(X)
    labels = ax.set_xticklabels([d.date() for d in list(stocksInfo.index)])
    for i, label in enumerate(labels):
        label.set_y(label.get_position()[1] - (i%2)*0.075)
    # plt.show()
    plt.savefig(img, format='png')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()

def generateProfitChart(value, stocks, stocksInfo, divideOption):
    img = io.BytesIO()
    stocks_list = getStockClose(stocks, stocksInfo)
    profits = []
    noOfShares = []
    valuePerStock = []
    if divideOption == 'Aggressively':
        for i in range(int(len(stocks) / 3)):
            valuePerStock.append(float(value) * 0.5 / (len(stocks) / 3))
            valuePerStock.append(float(value) * 0.3 / (len(stocks) / 3))
            valuePerStock.append(float(value) * 0.2 / (len(stocks) / 3))
    else: 
        valuePerStock = [float(value) / float(len(stocks)) for i in range(len(stocks))]
    idx = 0
    for s in range(len(stocks_list)):
        noOfShares.append(float(valuePerStock[idx]) / float(stocks_list[s][0]))
        idx += 1
    for d in range(len(stocks_list[0])):
        profit = 0
        for s in range(len(stocks_list)):
            profit += noOfShares[s] * stocks_list[s][d]
        profits.append(profit)
    fig = plt.figure()
    ax = fig.add_subplot()
    ax.plot(profits, 'o-')
    ax.set_xticks(np.arange(len(stocks_list[0])))
    labels = ax.set_xticklabels([d.date() for d in list(stocksInfo.index)])
    for i, label in enumerate(labels):
        label.set_y(label.get_position()[1] - (i%2)*0.075)
    # plt.show()
    plt.savefig(img, format='png')
    img.seek(0)
    return base64.b64encode(img.getvalue()).decode()

def generateStocksInfo(stocks, stocksInfo, value, divideOption):
    rst = ""
    rst += "<table id = 'table2'>"
    rst += "<tr><th>Symbol</th><th>Short Name</th><th>Last Price</th><th>Change</th><th>Time</th><th>Shares</th><th>Cost</th></tr>"
    idx = 0
    valuePerStock = []
    if divideOption == 'Aggressively':
        for i in range(int(len(stocks) / 3)):
            valuePerStock.append(float(value) * 0.5 / (len(stocks) / 3))
            valuePerStock.append(float(value) * 0.3 / (len(stocks) / 3))
            valuePerStock.append(float(value) * 0.2 / (len(stocks) / 3))
    else: 
        valuePerStock = [float(value) / float(len(stocks)) for i in range(len(stocks))]
    for s in stocks:
        entry = {}
        stock = yf.Ticker(s)
        entry['symbol'] = s
        entry['shortN'] = stock.info['shortName']
        entry['regularMP'] = stock.info['regularMarketPrice']
        change = round(stock.info['regularMarketPrice'] - stock.info['previousClose'], 2)
        if change > 0:
            entry['marketPC'] = '+' + str(change)
            entry['marketPCP'] = '+' + str(round(change / stock.info['previousClose'] * 100, 2))
        else: 
            entry['marketPC'] = str(change)
            entry['marketPCP'] = round(change / stock.info['previousClose'] * 100, 2)
        current = dt.datetime.now()
        entry['time'] = current.strftime("%a %b %d %H:%M:%S PDT %Y")
        entry['costs'] = valuePerStock[idx]
        # entry['costs'] = float(value) / len(stocks)
        entry['shares'] = entry['costs'] / entry['regularMP']
        rst += f"<tr><td>{entry['symbol']}</td><td>{entry['shortN']}</td><td>{entry['regularMP']:.02f}</td><td>{entry['marketPC']} {entry['marketPCP']}%</td><td>{entry['time']}</td><td>{entry['shares']:.02f}</td><td>${entry['costs']:.02f}</td></tr>"
        idx += 1
    rst += "</table>"
    return rst

@app.route('/', methods = ["GET", "POST"])
def home():
    return render_template("home.html")

@app.route('/stockportfolio', methods = ['POST', "GET"])
def generatePortfolio():
    s1 = request.form['strategy1']
    s2 = request.form['strategy2']
    divideOption = request.form['divideOption']
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

    stocks = getStock(s1, s2)
    stocksInfo = getStockInfo(stocks)
    stocksTable = generateStocksInfo(stocks, stocksInfo, value, divideOption)

    plot_url1 = generateBarChart(stocks, stocksInfo)

    plot_url2 = generateProfitChart(value, stocks, stocksInfo, divideOption)
    
    return render_template('stockportfolio.html', strategy1 = s1, strategy2 = s2, value = value, stocksTable = stocksTable, imagen1={'imagen1':plot_url1}, imagen2={'imagen2':plot_url2}) 
