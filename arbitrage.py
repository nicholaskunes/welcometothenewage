import requests
from pytz import utc
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import numpy as np

tickCount = 0;

def tick():
    global tickCount 
	
	#theory:
	#usd > alt > btc > usd
    
	
	#BITFINEX PUBLIC TICKER ALT/USD
	ticker_btcusd = requests.get('https://api.bitfinex.com/v1/pubticker/btcusd')
	ticker_zecusd = requests.get('https://api.bitfinex.com/v1/pubticker/zecusd')
	ticker_xmrusd = requests.get('https://api.bitfinex.com/v1/pubticker/xmrusd')
	ticker_xrpusd = requests.get('https://api.bitfinex.com/v1/pubticker/xrpusd')
	ticker_dshusd = requests.get('https://api.bitfinex.com/v1/pubticker/dshusd')
	
	#BITFINEX PUBLIC TICKER ALT/BTC
	ticker_zecbtc = requests.get('https://api.bitfinex.com/v1/pubticker/zecbtc')
	ticker_xmrbtc = requests.get('https://api.bitfinex.com/v1/pubticker/xmrbtc')
	ticker_xrpbtc = requests.get('https://api.bitfinex.com/v1/pubticker/xrpbtc')
	ticker_dshbtc = requests.get('https://api.bitfinex.com/v1/pubticker/dshbtc')
	
	#trigger theory:
	#threshold = (btc_price - ((1 / alt_btc_price) * alt_price)) - ((btc_price * 0.002) * 3);
	
	#BITFINEX TRIGGERS
    threshold_zec = (float(ticker_btcusd.json()['bid']) - ((1 / float(ticker_zecbtc.json()['bid'])) * float(ticker_zecusd.json()['bid']))) - ((float(ticker_btcusd.json()['bid']) * 0.002) * 3)

    
    #if price_btc.min() == float(ticker_btce.json()['btc_usd']['buy']):
    
    
	
	print("zec threshold is {}".format(threshold_zec))
    
    tickCount += 1


def main():
    scheduler = BlockingScheduler(timezone=utc)
    scheduler.add_job(tick, 'interval', seconds=1)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == '__main__':
    main()
