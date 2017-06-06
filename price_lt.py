import requests
from pytz import utc
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

tickCount = 0;

def tick():
    global tickCount 
    
    ticker_ltce = requests.get('https://btc-e.com/api/3/ticker/ltc_usd').json()
    ticker_btce = requests.get('https://btc-e.com/api/3/ticker/btc_usd').json()
    ticker_ethe = requests.get('https://btc-e.com/api/3/ticker/eth_usd').json()
    
    ticker_ltcfinex = requests.get('https://api.bitfinex.com/v1/pubticker/ltcusd').json()
    ticker_btcfinex = requests.get('https://api.bitfinex.com/v1/pubticker/btcusd').json()
    ticker_ethfinex = requests.get('https://api.bitfinex.com/v1/pubticker/ethusd').json()
    
    ticker_ltcdax = requests.get('https://api.gdax.com/products/LTC-USD/ticker').json()
    ticker_btcdax = requests.get('https://api.gdax.com/products/BTC-USD/ticker').json()
    ticker_ethdax = requests.get('https://api.gdax.com/products/ETH-USD/ticker').json()
    
    price_ltce = float(ticker_ltce['ltc_usd']['last'])
    price_btce = float(ticker_btce['btc_usd']['last'])
    price_ethe = float(ticker_ethe['eth_usd']['last'])
    
    price_ltcfinex = float(ticker_ltcfinex['last_price'])
    price_btcfinex = float(ticker_btcfinex['last_price'])
    price_ethfinex = float(ticker_ethfinex['last_price'])
    
    ticker_ltcdax = float(ticker_ltcdax['price'])
    ticker_btcdax = float(ticker_btcdax['price'])
    ticker_ethdax = float(ticker_ethdax['price'])
    
    tickCount += 1;
    print("ltce {} btce {} ethe {}\nltcfinex {} btcfinex {} ethfinex {}\nltcdax {} btcdax {} ethdax {}\n".format(price_ltce, price_btce, price_ethe, price_ltcfinex, price_btcfinex, price_ethfinex, price_ltcdax, price_btcdax, price_ethdax))


def main():
    """Run tick() at the interval of every ten seconds."""
    scheduler = BlockingScheduler(timezone=utc)
    scheduler.add_job(tick, 'interval', seconds=1)
    scheduler.start()


if __name__ == '__main__':
    main()
