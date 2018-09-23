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

while True:
		
	ticker = requests.get('https://api.gdax.com/products/BTC-USD/ticker').json()
	curprice = float(ticker['price'])
		
	print "change_variables = [ price: " + str(curprice) + " Δp " + str(end) + " ]"
		
	#np.savetxt("btc.csv", dps, delimiter=",")
 	#np.savetxt("prices.csv", prices3, delimiter=",")

 	#output = subprocess.check_output("curl --upload-file ./btc.csv https://transfer.sh/btc.csv", shell=True)
  	#output2 = subprocess.check_output("curl --upload-file ./prices.csv https://transfer.sh/prices.csv", shell=True)

 	#subprocess.call("rm btc.csv", shell=True)
	#subprocess.call("rm prices.csv", shell=True)
