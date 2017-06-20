import requests
from pytz import utc
from datetime import datetime
from pymongo import MongoClient
from apscheduler.schedulers.blocking import BlockingScheduler

client = MongoClient()
database = client['btc-e_db']
collection = database['historical_data']
tickCount = 0;


def tick():
    global tickCount 
    ticker = requests.get('https://btc-e.com/api/3/ticker/btc_usd').json()
    depth = requests.get('https://btc-e.com/api/3/depth/btc_usd').json()
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
