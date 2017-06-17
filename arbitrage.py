import requests
from pytz import utc
from pytz import timezone
import pytz
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
    threshold_xmr = (float(ticker_btcusd.json()['bid']) - ((1 / float(ticker_xmrbtc.json()['bid'])) * float(ticker_xmrusd.json()['bid']))) - ((float(ticker_btcusd.json()['bid']) * 0.002) * 3)
    threshold_xrp = (float(ticker_btcusd.json()['bid']) - ((1 / float(ticker_xrpbtc.json()['bid'])) * float(ticker_xrpusd.json()['bid']))) - ((float(ticker_btcusd.json()['bid']) * 0.002) * 3)
    threshold_dsh = (float(ticker_btcusd.json()['bid']) - ((1 / float(ticker_dshbtc.json()['bid'])) * float(ticker_dshusd.json()['bid']))) - ((float(ticker_btcusd.json()['bid']) * 0.002) * 3)

    threshold = 1
    
    thresholds = np.array([ threshold_zec, threshold_xmr, threshold_xrp, threshold_dsh ])
    
    if thresholds.max() == threshold_zec and threshold_zec >= threshold:
        altcoin = "zec"
    elif thresholds.max() == threshold_xmr and threshold_xmr >= threshold:
        altcoin = "xmr"
    elif thresholds.max() == threshold_xrp and threshold_xrp >= threshold:
        altcoin = "xrp"        
    elif thresholds.max() == threshold_dsh and threshold_dsh >= threshold:
        altcoin = "dsh"
    else
        altcoin = "null"
        
    date_format='%m/%d/%Y %H:%M:%S %Z'
    date = datetime.now(tz=pytz.utc)
    date = date.astimezone(timezone('US/Pacific'))
    
    if altcoin != "null":
        print("[{}] {} with profit {}".format(date.strftime(date_format), altcoin, thresholds.max()))
    
    tickCount += 1


def main():
    print("{0:{1}^60}".format("", "="))
    print("{0:{1}^60}".format(" arbitrage-bot ", "="))
    print("{0:{1}^60}".format(" usd > zec/xmr/xrp/dsh > btc > usd ", "="))
    print("{0:{1}^60}".format("", "="))
    scheduler = BlockingScheduler(timezone=utc)
    scheduler.add_job(tick, 'interval', seconds=10)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == '__main__':
    main()
