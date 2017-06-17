import requests
from pytz import utc
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import numpy as np

tickCount = 0;

def tick():
    global tickCount 
	
    ticker_ltce = requests.get('https://btc-e.com/api/3/ticker/ltc_usd')
    ticker_btce = requests.get('https://btc-e.com/api/3/ticker/btc_usd')
    ticker_ethe = requests.get('https://btc-e.com/api/3/ticker/eth_usd')
    
    ticker_ltcfinex = requests.get('https://api.bitfinex.com/v1/pubticker/ltcusd')
    ticker_btcfinex = requests.get('https://api.bitfinex.com/v1/pubticker/btcusd')
    ticker_ethfinex = requests.get('https://api.bitfinex.com/v1/pubticker/ethusd')
    
    ticker_ltcdax = requests.get('https://api.gdax.com/products/LTC-USD/ticker')
    ticker_btcdax = requests.get('https://api.gdax.com/products/BTC-USD/ticker')
    ticker_ethdax = requests.get('https://api.gdax.com/products/ETH-USD/ticker')
    
    price_ltce = float(ticker_ltce.json()['ltc_usd']['buy'])
    price_btce = float(ticker_btce.json()['btc_usd']['buy'])
    price_ethe = float(ticker_ethe.json()['eth_usd']['buy'])
    
    price_ltcfinex = float(ticker_ltcfinex.json()['bid'])
    price_btcfinex = float(ticker_btcfinex.json()['bid'])
    price_ethfinex = float(ticker_ethfinex.json()['bid'])
    
    price_ltcdax = float(ticker_ltcdax.json()['bid'])
    price_btcdax = float(ticker_btcdax.json()['bid'])
    price_ethdax = float(ticker_ethdax.json()['bid'])
    
    price_btc = np.array([ float(ticker_btce.json()['btc_usd']['buy']), 
                           float(ticker_btcfinex.json()['bid']), 
                           float(ticker_btcdax.json()['bid']) ])
    
    if price_btc.min() == float(ticker_btce.json()['btc_usd']['buy']):
        minimum_exchange = "btc-e"
        ltc_minratio = price_ltce / price_btce
        ltc_min = price_ltce
    elif price_btc.min() == float(ticker_btcfinex.json()['bid']):
        minimum_exchange = "bitfinex"
        ltc_minratio = price_ltcfinex / price_btcfinex
        ltc_min = price_ltcfinex
    elif price_btc.min() == float(ticker_btcdax.json()['bid']):
        minimum_exchange = "gdax"
        ltc_minratio = price_ltcdax / price_btcdax
        ltc_min = price_ltcdax
        
    if price_btc.max() == float(ticker_btce.json()['btc_usd']['buy']):
        maximum_exchange = "btc-e"
        ltc_maxratio = price_ltce / price_btce
        ltc_max = price_ltce
    elif price_btc.max() == float(ticker_btcfinex.json()['bid']):
        maximum_exchange = "bitfinex"
        ltc_maxratio = price_ltcfinex / price_btcfinex
        ltc_max = price_ltcfinex
    elif price_btc.max() == float(ticker_btcdax.json()['bid']):
        maximum_exchange = "gdax"
        ltc_maxratio = price_ltcdax / price_btcdax
        ltc_max = price_ltcdax
    
    
	
	print("minimum is {} USD at {} (LTC: {} USD) where maximum is {} USD at {} (LTC: {} USD) ltc proportion differential >> {:f}".format(price_btc.min(), minimum_exchange, ltc_min, price_btc.max(), maximum_exchange, ltc_max, ltc_maxratio - ltc_minratio))
    
    tickCount += 1;


def main():
    scheduler = BlockingScheduler(timezone=utc)
    scheduler.add_job(tick, 'interval', seconds=1)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == '__main__':
    main()
