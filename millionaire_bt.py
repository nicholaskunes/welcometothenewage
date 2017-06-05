# -*- coding: utf-8 -*-

from pymongo import MongoClient
from bayesian_regression import *
import time

client = MongoClient()
database = client['btc-e_db']
collection = database['historical_data']

  prices = []
  v_ask = []
  v_bid = []
  num_points = 777600
  for doc in collection.find().limit(num_points):
    prices.append(doc['price'])
    v_ask.append(doc['v_ask'])
    v_bid.append(doc['v_bid'])

[prices1, prices2, prices3] = np.array_split(prices, 3)

[v_bid1, v_bid2, v_bid3] = np.array_split(v_bid, 3)

[v_ask1, v_ask2, v_ask3] = np.array_split(v_ask, 3)

timeseries180 = generate_timeseries(prices1, 180)
timeseries360 = generate_timeseries(prices1, 360)
timeseries720 = generate_timeseries(prices1, 720)

centers180 = find_cluster_centers(timeseries180, 100)

s1 = choose_effective_centers(centers180, 20)

centers360 = find_cluster_centers(timeseries360, 100)

s2 = choose_effective_centers(centers360, 20)

centers720 = find_cluster_centers(timeseries720, 100)

s3 = choose_effective_centers(centers720, 20)

Dpi_r, Dp = linear_regression_vars(prices2, v_bid2, v_ask2, s1, s2, s3)

w = find_parameters_w(Dpi_r, Dp)

number = len(prices3)

print(number)

#dps = predict_dps(prices3, v_bid3, v_ask3, s1, s2, s3, w)

#np.savetxt("btc.csv", dps, delimiter=",")

#print("saved btc.csv")
