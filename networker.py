import requests
from pytz import utc
from pytz import timezone
import pytz
from datetime import datetime
from pymongo import MongoClient
from apscheduler.schedulers.blocking import BlockingScheduler

client = MongoClient()
database = client['bitfinex_db']
collection = database['historical_data']
tickCount = 0;


def tick():
    global tickCount 
    ticker = requests.get('https://api.bitfinex.com/v1/pubticker/btcusd').json()
    depth = requests.get('https://api.bitfinex.com/v1/book/btcusd').json()
    
    date_format='%m/%d/%Y %H:%M:%S %Z'
    date = datetime.now(tz=pytz.utc)
    date = date.astimezone(timezone('US/Pacific'))
    
    price = float(ticker['ask'])
    v_bid = sum([bid[1] for bid in depth['bids']])
    v_ask = sum([ask[1] for ask in depth['asks']]) 
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
