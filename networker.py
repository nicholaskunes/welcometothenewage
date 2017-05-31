"""Script to gather market data from OKCoin Spot Price API."""
import requests
from pytz import utc
from datetime import datetime
from pymongo import MongoClient
from apscheduler.schedulers.blocking import BlockingScheduler
import btceapi

client = MongoClient()
database = client['btc-e_db']
collection = database['historical_data']
tickCount = 0;


def tick():
    global tickCount
    
    #ticker = requests.get('https://www.okcoin.com/api/v1/ticker.do?symbol=btc_usd').json()
    #depth = requests.get('https://www.okcoin.com/api/v1/depth.do?symbol=btc_usd&size=60').json()
    #date = datetime.fromtimestamp(int(ticker['date']))
    #price = float(ticker['ticker']['last'])
    #v_bid = sum([bid[1] for bid in depth['bids']])
    #v_ask = sum([ask[1] for ask in depth['asks']])
    
    asks, bids = btceapi.getDepth(pair)

    print(len(asks), len(bids))

    ask_prices, ask_volumes = zip(*asks)
    bid_prices, bid_volumes = zip(*bids)
    
    print(ask_volumes);
    print(bid_volumes);

    
    #collection.insert({'date': date, 'price': price, 'v_bid': v_bid, 'v_ask': v_ask})
    tickCount += 1;
    print(tickCount)


def main():
    """Run tick() at the interval of every ten seconds."""
    scheduler = BlockingScheduler(timezone=utc)
    scheduler.add_job(tick, 'interval', seconds=10)
    scheduler.start()


if __name__ == '__main__':
    main()
