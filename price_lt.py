import requests
from pytz import utc
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

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
    
    price_ltce = float(ticker_ltce.json()['ltc_usd']['last'])
    price_btce = float(ticker_btce.json()['btc_usd']['last'])
    price_ethe = float(ticker_ethe.json()['eth_usd']['last'])
    
    price_ltcfinex = float(ticker_ltcfinex.json()['last_price'])
    price_btcfinex = float(ticker_btcfinex.json()['last_price'])
    price_ethfinex = float(ticker_ethfinex.json()['last_price'])
    
    price_ltcdax = float(ticker_ltcdax.json()['price'])
    price_btcdax = float(ticker_btcdax.json()['price'])
    price_ethdax = float(ticker_ethdax.json()['price'])
    
    tickCount += 1;
    print("ltce {} btce {} ethe {} [req {}ms]\nltcfinex {} btcfinex {} ethfinex {}[req {}ms]\nltcdax {} btcdax {} ethdax {}[req {}ms]\n".format(price_ltce, price_btce, price_ethe, (ticker_ethe.elapsed.total_seconds() * 1000), price_ltcfinex, price_btcfinex, price_ethfinex, (ticker_ethfinex.elapsed.total_seconds() * 1000), price_ltcdax, price_btcdax, price_ethdax, (ticker_ethdax.elapsed.total_seconds() * 1000)))


def main():
    """Run tick() at the interval of every ten seconds."""
    scheduler = BlockingScheduler(timezone=utc)
    scheduler.add_job(tick, 'interval', seconds=1)
    scheduler.start()


if __name__ == '__main__':
    main()
