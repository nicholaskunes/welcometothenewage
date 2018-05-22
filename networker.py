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
    ticker = requests.get('https://wex.nz/api/3/ticker/btc_usd').json()
    depth = requests.get('https://wex.nz/api/3/depth/btc_usd?limit=60').json()
    date = datetime.fromtimestamp(int(ticker['btc_usd']['updated']))
    price = float(ticker['btc_usd']['last'])
    v_bid = sum([bid[1] for bid in depth['btc_usd']['bids']])
    v_ask = sum([ask[1] for ask in depth['btc_usd']['asks']])
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
