import yfinance as yf
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

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
    if s1 == 'ethical' or s2 == 'ethical':
        stocks += ethical
    if s1 == 'growth' or s2 == 'growth':
        stocks += growth
    if s1 == 'index' or s2 == 'index':
        stocks += index
    if s1 == 'quality' or s2 == 'quality':
        stocks += quality
    if s1 == 'value' or s2 == 'value':
        stocks += value
    return stocks

def getStockInfo(stocks):
    stocksInfo = yf.download(" ".join(stocks), start=last_n_day, end=todays_date)
    return stocksInfo

def getStockClose(stocksInfo):
    stocks_list = []
    for s in range(len(stocks)):
        stock_list = []
        for d in range(last_n_days - 2):
            stock_list.append(stocksInfo.iloc[d][s+len(stocks)])
        stocks_list.append(stock_list)
    return stocks_list

def generateBarChart(stocks, stocksInfo):
    stocks_list = getStockClose(stocksInfo)
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
    plt.show()

def generateProfitChart(amount, stocks, stocksInfo):
    stocks_list = getStockClose(stocksInfo)
    profits = []
    noOfShares = []
    amountPerStock = float(amount) / float(len(stocks))
    for s in range(len(stocks_list)):
        noOfShares.append(float(amountPerStock) / float(stocks_list[s][0]))
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
    plt.show()

if __name__ == '__main__':
    print("Please input the first strategy: ")
    print("ethical, growth, index, quality, or value")
    s1 = input()
    print("Please input the second strategy: ")
    print("Enter 'none' it unnecessarty")
    s2 = input()
    print("Please input the amount ($): ")
    print("minimum is 5000")
    amount = input()

    stocks = getStock(s1, s2)
    stocksInfo = getStockInfo(stocks)
    generateBarChart(stocks, stocksInfo)

    generateProfitChart(amount, stocks, stocksInfo)
