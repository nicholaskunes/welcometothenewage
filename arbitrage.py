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

#usd > alt > btc > usd
#usd > btc > alt > usd

#-0.01

def zec_cycle():
    global cycling    
    cycling = True

    ticker = requests.get('https://api.bitfinex.com/v1/pubticker/zecbtc') 
    ticker2 = requests.get('https://api.bitfinex.com/v1/pubticker/btcusd')
    proportion = float((wallet_balances("usd") / float(ticker2.json()['ask'])) - ((wallet_balances("usd") / float(ticker2.json()['ask'])) * 0.002))
    
    print("[calc] pro {} balance {} price {}".format(proportion, wallet_balances("usd"), float(ticker2.json()['ask'])))

    order = place_order(str(proportion), str(time.time()), "buy", "exchange market", "btcusd")
    print(order['order_id'])

    while order_status(order['order_id']) == True:
        print("order status false 1")
        time.sleep(0.2)
        
    proportion = float((wallet_balances("btc") / float(ticker.json()['ask'])) - ((wallet_balances("btc") / float(ticker.json()['ask'])) * 0.002))

    order = place_order(str(proportion), str(time.time()), "buy", "exchange market", "zecbtc")
    print(order['order_id'])
    
    while order_status(order['order_id']) == True:
        print("order status false 2")
        time.sleep(0.2)
        
    proportion = float((wallet_balances("zec") - (wallet_balances("zec") * 0.002)))
    
    order = place_order(str(proportion), str(time.time()), "sell", "exchange market", "zecusd")
    print(order['order_id'])
            
    cycling = False
    
def xmr_cycle():
    global cycling    
    cycling = True

    ticker = requests.get('https://api.bitfinex.com/v1/pubticker/xmrbtc') 
    ticker2 = requests.get('https://api.bitfinex.com/v1/pubticker/btcusd')
    proportion = float((wallet_balances("usd") / float(ticker2.json()['ask'])) - ((wallet_balances("usd") / float(ticker2.json()['ask'])) * 0.002))
    
    print("[calc] pro {} balance {} price {}".format(proportion, wallet_balances("usd"), float(ticker2.json()['ask'])))

    order = place_order(str(proportion), str(time.time()), "buy", "exchange market", "btcusd")
    print(order['order_id'])

    while order_status(order['order_id']) == True:
        print("order status false 1")
        time.sleep(0.2)
        
    proportion = float((wallet_balances("btc") / float(ticker.json()['ask'])) - ((wallet_balances("btc") / float(ticker.json()['ask'])) * 0.002))

    order = place_order(str(proportion), str(time.time()), "buy", "exchange market", "xmrbtc")
    print(order['order_id'])
    
    while order_status(order['order_id']) == True:
        print("order status false 2")
        time.sleep(0.2)
        
    proportion = float((wallet_balances("xmr") - (wallet_balances("xmr") * 0.002)))
    
    order = place_order(str(proportion), str(time.time()), "sell", "exchange market", "xmrusd")
    print(order['order_id'])
            
    cycling = False
    
def xrp_cycle():
    global cycling    
    cycling = True

    ticker = requests.get('https://api.bitfinex.com/v1/pubticker/xrpbtc') 
    ticker2 = requests.get('https://api.bitfinex.com/v1/pubticker/btcusd')
    proportion = float((wallet_balances("usd") / float(ticker2.json()['ask'])) - ((wallet_balances("usd") / float(ticker2.json()['ask'])) * 0.002))
    
    print("[calc] pro {} balance {} price {}".format(proportion, wallet_balances("usd"), float(ticker2.json()['ask'])))

    order = place_order(str(proportion), str(time.time()), "buy", "exchange market", "btcusd")
    print(order['order_id'])

    while order_status(order['order_id']) == True:
        print("order status false 1")
        time.sleep(0.2)
        
    proportion = float((wallet_balances("btc") / float(ticker.json()['ask'])) - ((wallet_balances("btc") / float(ticker.json()['ask'])) * 0.002))

    order = place_order(str(proportion), str(time.time()), "buy", "exchange market", "xrpbtc")
    print(order['order_id'])
    
    while order_status(order['order_id']) == True:
        print("order status false 2")
        time.sleep(0.2)
        
    proportion = float((wallet_balances("xrp") - (wallet_balances("xrp") * 0.002)))
    
    order = place_order(str(proportion), str(time.time()), "sell", "exchange market", "xrpusd")
    print(order['order_id'])
            
    cycling = False

def dsh_cycle():
    global cycling    
    cycling = True

    ticker = requests.get('https://api.bitfinex.com/v1/pubticker/dshbtc') 
    ticker2 = requests.get('https://api.bitfinex.com/v1/pubticker/btcusd')
    proportion = float((wallet_balances("usd") / float(ticker2.json()['ask'])) - ((wallet_balances("usd") / float(ticker2.json()['ask'])) * 0.002))
    
    print("[calc] pro {} balance {} price {}".format(proportion, wallet_balances("usd"), float(ticker2.json()['ask'])))

    order = place_order(str(proportion), str(time.time()), "buy", "exchange market", "btcusd")
    print(order['order_id'])

    while order_status(order['order_id']) == True:
        print("order status false 1")
        time.sleep(0.2)
        
    proportion = float((wallet_balances("btc") / float(ticker.json()['ask'])) - ((wallet_balances("btc") / float(ticker.json()['ask'])) * 0.002))

    order = place_order(str(proportion), str(time.time()), "buy", "exchange market", "dshbtc")
    print(order['order_id'])
    
    while order_status(order['order_id']) == True:
        print("order status false 2")
        time.sleep(0.2)
        
    proportion = float((wallet_balances("dsh") - (wallet_balances("dsh") * 0.002)))
    
    order = place_order(str(proportion), str(time.time()), "sell", "exchange market", "dshusd")
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
    #($bitfinex_btc_ask-((1/$bitfinex_eth_crypto_ask)*$bitfinex_eth_bid))-(($bitfinex_btc_ask*0.002)*3);
        
    zec1 = 1 - (1 * 0.002)
    zec2 = zec1 / float(ticker_zecbtc.json()['ask'])
    zec3 = zec2 - (zec2 * 0.002)
    zec4 = zec3 * float(ticker_zecusd.json()['ask'])
    zec5 = zec4 - (zec4 * 0.002)
    threshold_zec = zec5 - float(ticker_btcusd.json()['ask'])
    
    xmr1 = 1 - (1 * 0.002)
    xmr2 = xmr1 / float(ticker_xmrbtc.json()['ask'])
    xmr3 = xmr2 - (xmr2 * 0.002)
    xmr4 = xmr3 * float(ticker_xmrusd.json()['ask'])
    xmr5 = xmr4 - (xmr4 * 0.002)
    threshold_xmr = xmr5 - float(ticker_btcusd.json()['ask'])
    
    xrp1 = 1 - (1 * 0.002)
    xrp2 = xrp1 / float(ticker_xrpbtc.json()['ask'])
    xrp3 = xrp2 - (xrp2 * 0.002)
    xrp4 = xrp3 * float(ticker_xrpusd.json()['ask'])
    xrp5 = xrp4 - (xrp4 * 0.002)
    threshold_xrp = xrp5 - float(ticker_btcusd.json()['ask'])
    
    dsh1 = 1 - (1 * 0.002)
    dsh2 = dsh1 / float(ticker_dshbtc.json()['ask'])
    dsh3 = dsh2 - (dsh2 * 0.002)
    dsh4 = dsh3 * float(ticker_dshusd.json()['ask'])
    dsh5 = dsh4 - (dsh4 * 0.002)
    threshold_dsh = dsh5 - float(ticker_btcusd.json()['ask'])
    
    threshold = 200
    
    thresholds = np.array([ threshold_zec, threshold_xmr, threshold_xrp, threshold_dsh ])
            
    if thresholds.max() == threshold_zec and threshold_zec >= threshold and cycling == False:
        altcoin = "zec"
        t = threading.Thread(target=zec_cycle)
        #t.start()    
    elif thresholds.max() == threshold_xmr and threshold_xmr >= threshold and cycling == False:
        altcoin = "xmr"
        t = threading.Thread(target=xmr_cycle)
        #t.start() 
    elif thresholds.max() == threshold_xrp and threshold_xrp >= threshold and cycling == False:
        altcoin = "xrp"      
        t = threading.Thread(target=xrp_cycle)  
        #t.start()         
    elif thresholds.max() == threshold_dsh and threshold_dsh >= threshold and cycling == False:
        altcoin = "dsh"
        t = threading.Thread(target=dsh_cycle)
        #t.start() 
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
        print("[{}] tick {} -- nothing... zec {} xmr {} xrp {} dsh {}".format(date.strftime(date_format), tickCount, threshold_zec, threshold_xmr, threshold_xrp, threshold_dsh))
        
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
