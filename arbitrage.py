import requests
from pytz import utc
from pytz import timezone
import pytz
from datetime import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
import numpy as np
import threading
import time
import base64
import hmac
import hashlib
import json

tickCount = 0
cycling = False

def zec_cycle():
    global cycling    
    cycling = True

    ticker = requests.get('https://api.bitfinex.com/v1/pubticker/zecusd') 
    ticker2 = requests.get('https://api.bitfinex.com/v1/pubticker/btcusd')
    proportion = (wallet_balances("usd") / float(ticker.json()['mid']))
    
    print("[calc] pro {} balance {} price {}".format(proportion, wallet_balances("usd"), float(ticker.json()['mid'])))

    order = place_order(str(proportion), str(time.time()), "buy", "exchange market", "zecusd")
    print(order['order_id'])

    while order_status(order['order_id']) == True:
        print("order status false 1")
        time.sleep(0.2)
        
    proportion = (wallet_balances("zec"))

    order = place_order(str(proportion), str(time.time()), "sell", "exchange market", "zecbtc")
    print(order['order_id'])
    
    while order_status(order['order_id']) == True:
        print("order status false 2")
        time.sleep(0.2)
        
    proportion_btc = (wallet_balances("btc"))
    
    order = place_order(str(proportion_btc), str(time.time()), "sell", "exchange market", "btcusd")
    print(order['order_id'])
            
    cycling = False
    
def xmr_cycle():
    global cycling    
    cycling = True

    ticker = requests.get('https://api.bitfinex.com/v1/pubticker/xmrusd')    
    ticker2 = requests.get('https://api.bitfinex.com/v1/pubticker/btcusd')
    proportion = (wallet_balances("usd") / float(ticker.json()['mid']))
    
    print("[calc] pro {} balance {} price {}".format(proportion, wallet_balances("usd"), float(ticker.json()['mid'])))

    order = place_order(str(proportion), str(time.time()), "buy", "exchange market", "xmrusd")
    print(order['order_id'])
    
    while order_status(order['order_id']) == True:
        print("order status false 1")
        time.sleep(0.2)
        
    proportion = (wallet_balances("xmr"))

    order = place_order(str(proportion), str(time.time()), "sell", "exchange market", "xmrbtc")
    print(order['order_id'])
    
    while order_status(order['order_id']) == True:
        print("order status false 2")
        time.sleep(0.2)
        
    proportion_btc = (wallet_balances("btc"))
    
    order = place_order(str(proportion_btc), str(time.time()), "sell", "exchange market", "btcusd")
    print(order['order_id'])
            
    cycling = False
    
def xrp_cycle():
    global cycling    
    cycling = True

    ticker = requests.get('https://api.bitfinex.com/v1/pubticker/xrpusd')    
    ticker2 = requests.get('https://api.bitfinex.com/v1/pubticker/btcusd')
    proportion = (wallet_balances("usd") / float(ticker.json()['mid']))
    
    print("[calc] pro {} balance {} price {}".format(proportion, wallet_balances("usd"), float(ticker.json()['mid'])))

    order = place_order(str(proportion), str(time.time()), "buy", "exchange market", "xrpusd")
    print(order['order_id'])
    
    proportion = (wallet_balances("xrp"))
    
    while order_status(order['order_id']) == True:
        print("order status false 1")
        time.sleep(0.2)
        
    order = place_order(str(proportion), str(time.time()), "sell", "exchange market", "xrpbtc")
    print(order['order_id'])
    
    while order_status(order['order_id']) == True:
        print("order status false 2")
        time.sleep(0.2)
        
    proportion_btc = (wallet_balances("btc"))
        
    order = place_order(str(proportion_btc), str(time.time()), "sell", "exchange market", "btcusd")
    print(order['order_id'])
            
    cycling = False

def dsh_cycle():
    global cycling    
    cycling = True

    ticker = requests.get('https://api.bitfinex.com/v1/pubticker/dshusd')    
    ticker2 = requests.get('https://api.bitfinex.com/v1/pubticker/btcusd')
    proportion = (wallet_balances("usd") / float(ticker.json()['mid']))
    
    print("[calc] pro {} balance {} price {}".format(proportion, wallet_balances("usd"), float(ticker.json()['mid'])))

    order = place_order(str(proportion), str(time.time()), "buy", "exchange market", "dshusd")
    print(order['order_id'])
    
    proportion = (wallet_balances("dsh"))
    
    while order_status(order['order_id']) == True:
        print("order status false 1")
        time.sleep(0.2)
        
    order = place_order(str(proportion), str(time.time()), "sell", "exchange market", "dshbtc")
    print(order['order_id'])
    
    while order_status(order['order_id']) == True:
        print("order status false 2")
        time.sleep(0.2)
        
    proportion_btc = (wallet_balances("btc"))
        
    order = place_order(str(proportion_btc), str(time.time()), "sell", "exchange market", "btcusd")
    print(order['order_id'])
            
    cycling = False   


def sign_payload(payload):
    j = json.dumps(payload)
    data = base64.standard_b64encode(j.encode('utf8'))

    h = hmac.new("80VnuuA3vQThm2lTQJBDEsLgGPisBxg2WVFi2ZXtoRO".encode('utf8'), data, hashlib.sha384)
    signature = h.hexdigest()
    return {
        "X-BFX-APIKEY": "il3r5zm6WVxkfBsbso1JG7XvekPBmTGYEHWeH20TQ6p",
        "X-BFX-SIGNATURE": signature,
        "X-BFX-PAYLOAD": data
    } 

def place_order(amount, price, side, ord_type, symbol, exchange='bitfinex'):
    payload = {
        "request": "/v1/order/new",
        "nonce": str(time.time() + 2000),
        "symbol": symbol,
        "amount": amount,
        "price": price,
        "exchange": exchange,
        "side": side,
        "type": ord_type
    }

    signed_payload = sign_payload(payload)
    r = requests.post("https://api.bitfinex.com/v1/order/new", headers=signed_payload, verify=True)
    json_resp = r.json()

    try:
        json_resp['order_id']
    except:
        print(json_resp)
        return json_resp
    return json_resp    

def wallet_balances(currency):
    payload = {
        "request": "/v1/balances",
        "nonce": str(time.time() + 2000)
    }

    signed_payload = sign_payload(payload)
    r = requests.post("https://api.bitfinex.com/v1/balances", headers=signed_payload, verify=True)
    json_resp = r.json()
       
    for wallet in json_resp:
        if wallet['type'] == "exchange":
           if wallet['currency'] == currency:
                return float(wallet['available'])
    
    return -1
        
def order_status(order_id):
    payload = {
        "request": "/v1/order/status",
        "nonce": str(time.time() + 2000),
        "order_id": order_id
    }

    signed_payload = sign_payload(payload)
    r = requests.post("https://api.bitfinex.com/v1/order/status", headers=signed_payload, verify=True)
    json_resp = r.json()
    
    try:
        json_resp['is_live']
    except:
        print(json_resp)
        return True
    return json_resp['is_live']

def tick():
    global tickCount 
    global cycling
    
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
            
    if thresholds.max() == threshold_zec and threshold_zec >= threshold and cycling == False:
        altcoin = "zec"
        t = threading.Thread(target=zec_cycle)
        t.start()    
    elif thresholds.max() == threshold_xmr and threshold_xmr >= threshold and cycling == False:
        altcoin = "xmr"
        t = threading.Thread(target=xmr_cycle)
        t.start() 
    elif thresholds.max() == threshold_xrp and threshold_xrp >= threshold and cycling == False:
        altcoin = "xrp"      
        t = threading.Thread(target=xrp_cycle)  
        t.start()         
    elif thresholds.max() == threshold_dsh and threshold_dsh >= threshold and cycling == False:
        altcoin = "dsh"
        t = threading.Thread(target=dsh_cycle)
        t.start() 
    elif cycling == False:
        altcoin = "null"
    else:
        altcoin = "cycling"
        
    date_format='%m/%d/%Y %H:%M:%S %Z'
    date = datetime.now(tz=pytz.utc)
    date = date.astimezone(timezone('US/Pacific'))
    
    if altcoin != "null" and altcoin != "cycling":
        print("[{}] started cycle on {} with profit {} on tick {}".format(date.strftime(date_format), altcoin, thresholds.max(), tickCount))
    elif altcoin == "cycling":
        print("[{}] currently cycling...".format(date.strftime(date_format)))
    else:
        print("[{}] tick {} -- nothing... zec {}".format(date.strftime(date_format), tickCount, threshold_zec))
        
    tickCount += 1


def main():
    print("{0:{1}^60}".format("", "="))
    print("{0:{1}^60}".format(" arbitrage-bot ", "="))
    print("{0:{1}^60}".format(" usd > zec/xmr/xrp/dsh > btc > usd ", "="))
    print("{0:{1}^60}".format("", "="))
    
    #order = place_order("0.0149", str(time.time()), "sell", "exchange market", "btcusd")
    #order = place_order("0.0149", str(time.time()), "buy", "exchange market", "btcusd")   
    #print(order)
    
    scheduler = BlockingScheduler(timezone=utc)
    scheduler.add_job(tick, 'interval', seconds=10)
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        pass


if __name__ == '__main__':
    main()
