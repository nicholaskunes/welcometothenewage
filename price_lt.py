import requests
from pytz import utc
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler

tickCount = 0;


def tick():
    global tickCount 
    ticker = requests.get('https://btc-e.com/api/3/ticker/ltc_usd').json()
    price = float(ticker['ltc_usd']['last'])
    tickCount += 1;
    print("##LTC## {}".format(price))


def main():
    """Run tick() at the interval of every ten seconds."""
    scheduler = BlockingScheduler(timezone=utc)
    scheduler.add_job(tick, 'interval', seconds=10)
    scheduler.start()


if __name__ == '__main__':
    main()
