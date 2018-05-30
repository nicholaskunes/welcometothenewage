# -*- coding: utf-8 -*-
from pymongo import MongoClient
from bayesian_regression import *
import subprocess
import time
import requests
from datetime import datetime
from tqdm import tqdm

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

	#dps = predict_dps(prices3, v_bid3, v_ask3, s1, s2, s3, w)
	iterator = 0
	completion = 0
    	position = 0
	balance = 0
	for i in tqdm(range(0, 720, 1)): 
		completion += 1
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

		end = live_trade(prices3, v_bid3, v_ask3, s1, s2, s3, w, t=0.0001, step=1)
		
		ticker = requests.get('https://api.gdax.com/products/BTC-USD/ticker').json()
		curprice = float(ticker['price'])
		
        	# BUY
    		if end > 0.15 and position <= 0:
			iterator += 1
    			position += 1
    		        balance -= curprice
			#print "[" + str(iterator) + " BUY] " + str(datetime.now()) + " predict t+10s Δp " + str(end) + " $" + str(round(balance, 5))
        	# SELL
    		if end < -0.15 and position >= 0:
			iterator += 1
    			position -= 1
    			balance += curprice
			#print "[" + str(iterator) + " SELL] " + str(datetime.now()) + " predict t+10s Δp " + str(end) + " $" + str(round(balance, 5))
		time.sleep(10)
		
	ticker = requests.get('https://api.gdax.com/products/BTC-USD/ticker').json()

	# SELL
    	if position == 1:
        	balance += float(ticker['price'])
    	# PAY BROKER BACK
    	if position == -1:
		balance -= float(ticker['price'])
		
	print "[series profit: $" + str(balance) + " ] " + "trade count: " + str(iterator)
		
	#np.savetxt("btc.csv", dps, delimiter=",")
 	#np.savetxt("prices.csv", prices3, delimiter=",")

 	#output = subprocess.check_output("curl --upload-file ./btc.csv https://transfer.sh/btc.csv", shell=True)
  	#output2 = subprocess.check_output("curl --upload-file ./prices.csv https://transfer.sh/prices.csv", shell=True)

 	#subprocess.call("rm btc.csv", shell=True)
	#subprocess.call("rm prices.csv", shell=True)
