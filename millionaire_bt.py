# -*- coding: utf-8 -*-
from __future__ import print_function
import sys
from pymongo import MongoClient
from bayesian_regression import *
import subprocess
import time
import requests
from datetime import datetime

client = MongoClient()
database = client['predictor']
collection = database['gdax']

positive = 0

while True:
	prices = []
	v_ask = []
	v_bid = []
	num_points = 777600
	for doc in collection.find().limit(num_points):
		prices.append(doc['price'])
		v_ask.append(doc['v_ask'])
		v_bid.append(doc['v_bid'])

	[prices1, prices2] = np.array_split(prices, 2)
	[v_bid1, v_bid2] = np.array_split(v_bid, 2)
	[v_ask1, v_ask2] = np.array_split(v_ask, 2)
	
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

	#dps = predict_dps(prices3, v_bid3, v_ask3, s1, s2, s3, w)
	iterator = 0
    	position = 0
	balance = 0
	for i in range(0, 720, 1): 
		iterator += 1
		prices = []
		v_ask = []
		v_bid = []
		num_points = 777600
		for doc in collection.find().limit(num_points):
			prices.append(doc['price'])
			v_ask.append(doc['v_ask'])
			v_bid.append(doc['v_bid'])

		[prices1, prices2] = np.array_split(prices, 2)
		[v_bid1, v_bid2] = np.array_split(v_bid, 2)
		[v_ask1, v_ask2] = np.array_split(v_ask, 2)

		end = live_trade(prices2, v_bid2, v_ask2, s1, s2, s3, w, t=0.0001, step=1)
		
		ticker = requests.get('https://api.gdax.com/products/BTC-USD/ticker').json()
		curprice = float(ticker['price'])
		
        	# long position - BUY
    		if end > 0.0001 and position <= 0:
    			position += 1
    		        balance -= curprice
			print("[trade " + str(iterator) + " BUY]" + " timestamp: " + str(datetime.now()) + " delta p @ t+10s: " + str(end) + " USD: $" + str(float(balance)))
        	# short position - SELL
    		if end < -0.0001 and position >= 0:
    			position -= 1
    			balance += curprice
			print("[trade " + str(iterator) + " SELL]" + " timestamp: " + str(datetime.now()) + " delta p @ t+10s: " + str(end) + " USD: $" + str(float(balance)))
		print(str(end) + ", ", end='')
		sys.stdout.flush()
		time.sleep(10)
		
	ticker = requests.get('https://api.gdax.com/products/BTC-USD/ticker').json()

	# sell what you bought
    	if position == 1:
        	balance += float(ticker['price'])
    	# pay back what you borrowed
    	if position == -1:
		balance -= float(ticker['price'])
		
	print("[series profit: $" + str(balance) + " ] " + "trade count: " + str(iterator))
		
	#np.savetxt("btc.csv", dps, delimiter=",")
 	#np.savetxt("prices.csv", prices3, delimiter=",")

 	#output = subprocess.check_output("curl --upload-file ./btc.csv https://transfer.sh/btc.csv", shell=True)
  	#output2 = subprocess.check_output("curl --upload-file ./prices.csv https://transfer.sh/prices.csv", shell=True)

 	#subprocess.call("rm btc.csv", shell=True)
	#subprocess.call("rm prices.csv", shell=True)
