# -*- coding: utf-8 -*-

from pymongo import MongoClient
from bayesian_regression import *
import time
import requests
from pytz import utc
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

client = MongoClient()
database = client['ltc-e_db']
collection = database['historical_data']

# Retrieve price, v_ask, and v_bid data points from the database.
prices = []
v_ask = []
v_bid = []
num_points = 777600
for doc in collection.find().limit(num_points):
    prices.append(doc['price'])
    v_ask.append(doc['v_ask'])
    v_bid.append(doc['v_bid'])

# Divide prices into three, roughly equal sized, periods:
# prices1, prices2, and prices3.

[prices1, prices2, prices3] = np.array_split(prices, 3)

# Divide v_bid into three, roughly equal sized, periods:
# v_bid1, v_bid2, and v_bid3.
[v_bid1, v_bid2, v_bid3] = np.array_split(v_bid, 3)

# Divide v_ask into three, roughly equal sized, periods:
# v_ask1, v_ask2, and v_ask3.
[v_ask1, v_ask2, v_ask3] = np.array_split(v_ask, 3)

# Use the first time period (prices1) to generate all possible time series of
# appropriate length (180, 360, and 720).
timeseries180 = generate_timeseries(prices1, 180)
timeseries360 = generate_timeseries(prices1, 360)
timeseries720 = generate_timeseries(prices1, 720)

# Cluster timeseries180 in 100 clusters using k-means, return the cluster
# centers (centers180), and choose the 20 most effective centers (s1).
centers180 = find_cluster_centers(timeseries180, 100)
s1 = choose_effective_centers(centers180, 20)

centers360 = find_cluster_centers(timeseries360, 100)
s2 = choose_effective_centers(centers360, 20)

centers720 = find_cluster_centers(timeseries720, 100)
s3 = choose_effective_centers(centers720, 20)

# Use the second time period to generate the independent and dependent
# variables in the linear regression model:
# Δp = w0 + w1 * Δp1 + w2 * Δp2 + w3 * Δp3 + w4 * r.
Dpi_r, Dp = linear_regression_vars(prices2, v_bid2, v_ask2, s1, s2, s3)

# Find the parameter values w (w0, w1, w2, w3, w4).
w = find_parameters_w(Dpi_r, Dp)

# Predict average price changes over the third time period.
dps = predict_dps(prices3, v_bid3, v_ask3, s1, s2, s3, w)

ticker = requests.get('https://btc-e.com/api/3/ticker/ltc_usd').json()
price = float(ticker['ltc_usd']['last'])

btce_fee = 0.002
bitcoin_amount = 1
trade_count = 0
dp_count = 0
position = 0
revenue_btc = bitcoin_amount
revenue_usd = price
t = 0.0035
for i in range(0, 721, 1):
    dp_count += 1
    # BUY position
    if dps[i] > t and position <= 0:
        trade_count += 1
        position += 1
        ticker = requests.get('https://btc-e.com/api/3/ticker/ltc_usd').json()
        date = datetime.fromtimestamp(int(ticker['ltc_usd']['updated']))
        price = float(ticker['ltc_usd']['last'])
        revenue_usd -= (bitcoin_amount - (bitcoin_amount * btce_fee)) * price
        revenue_btc += bitcoin_amount
        print("[SESSION-{}-{}] BOUGHT {} BTC at ${} USD and currently hold $ {}, BTC {}".format(date, dp_count, bitcoin_amount, price, revenue_usd, revenue_btc))
    # SELL position
    if dps[i] < -t and position >= 0:
        trade_count += 1
        position -= 1
        ticker = requests.get('https://btc-e.com/api/3/ticker/ltc_usd').json()
        date = datetime.fromtimestamp(int(ticker['ltc_usd']['updated']))
        price = float(ticker['ltc_usd']['last'])
        revenue_btc -= bitcoin_amount
        revenue_usd += (bitcoin_amount - (bitcoin_amount * btce_fee)) * price
        print("[SESSION-{}-{}] SOLD {} BTC at ${} USD and currently hold $ {}, BTC {}".format(date, dp_count, bitcoin_amount, price, revenue_usd, revenue_btc))
        # sell what you bought
    time.sleep(10)
    
ticker = requests.get('https://btc-e.com/api/3/ticker/ltc_usd').json()
price = float(ticker['ltc_usd']['last'])
date = datetime.fromtimestamp(int(ticker['ltc_usd']['updated']))
print("###---SESSION COMPLETE---###")
print("[SESSION-{}] # of trades: {} revenue: {} {} last price for profit calc: {}".format(date, trade_count, revenue_btc, revenue_usd, price))
