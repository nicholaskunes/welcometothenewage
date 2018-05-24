"""Script to gather market data from OKCoin Spot Price API."""
import requests
from pytz import utc
from datetime import datetime
from pymongo import MongoClient
from apscheduler.schedulers.blocking import BlockingScheduler
import logging

client = MongoClient()
database = client['btc-e_db']
collection = database['historical_data']
tickCount = 0;

logging.basicConfig()

def tick():
    global tickCount 
    ticker = requests.get('https://api.gdax.com/products/BTC-USD/ticker').json()
    depth = requests.get('https://api.gdax.com/products/BTC-USD/book?level=2').json()
    date = datetime.strptime(ticker['time'], "%Y-%m-%dT%H:%M:%S.%fZ")
    price = float(ticker['price'])
    v_bid = sum([float(bid[1]) for bid in depth['bids']])
    v_ask = sum([float(ask[1]) for ask in depth['asks']])
    collection.insert({'date': date, 'price': price, 'v_bid': v_bid, 'v_ask': v_ask})
    tickCount += 1;
    print(tickCount)
    print("date: {} price: {} v_bid: {} v_ask: {}".format(date, price, v_bid, v_ask))


def main():
    """Run tick() at the interval of every ten seconds."""
    scheduler = BlockingScheduler(timezone=utc)
    scheduler.add_job(tick, 'interval', seconds=10)
    scheduler.start()


if __name__ == '__main__':
    main()
