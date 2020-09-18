
import time
import argparse
import requests
import json
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from datetime import datetime


BITCOIN_PRICE_THRESHOLD = 10000
BITCOIN_API_URL = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'
IFTTT_WEBHOOKS_URL = "https://maker.ifttt.com/trigger/Bit_Coin/with/key/bwBBdvI5locB8l3AqREhx9"
def get_latest_bitcoin_price():
    # coinmarketcap api url
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {"start": "1", "limit": "5000", "convert": "USD"}

    headers = {
        'Accepts': 'application/json',
        # coinmarketcap individual key
        'X-CMC_PRO_API_KEY': '1d37004a-3dd9-42e3-971e-2a86ed78dfa7',
    }

    session = Session()
    session.headers.update(headers)

    try:
        response = session.get(url, params=parameters)
        # getting the json data
        data = json.loads(response.text)
    # return data
    except (ConnectionError, Timeout, TooManyRedirects) as e:
        print(e)
    print("BTC Price", float(data['data'][0]['quote']['USD']['price']))
    return float(data['data'][0]['quote']['USD']['price'])
  
def post_ifttt_webhook(event, value):
    data = {'value1': value}  
    ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event)  
    requests.post(ifttt_event_url, json=data)  

def format_bitcoin_history(bitcoin_history):
    rows = []
    for bitcoin_price in bitcoin_history:
        date = bitcoin_price['date'].strftime('%d.%m.%Y %H:%M')  
        price = bitcoin_price['price']
        price = round(price, 2)
        
        row = '{}: $<b>{}</b>'.format(date, price)  
        rows.append(row)


    return '<br>'.join(rows)

def main():
    bitcoin_history = []
    while True:
        price = get_latest_bitcoin_price()
        price = round(price, 2)
        date = datetime.now()
        bitcoin_history.append({'date': date, 'price': price})

        # Send an emergency notification
        if price < BITCOIN_PRICE_THRESHOLD:
            post_ifttt_webhook('bitcoin_price_emergency', price)

        # Send a Telegram notification
        if len(bitcoin_history) == 5:  # Once we have 5 items in our bitcoin_history send an update
            post_ifttt_webhook('bitcoin_price_update', format_bitcoin_history(bitcoin_history))
            # Reset the history
            bitcoin_history = []

        time.sleep(5 * 60)    

if __name__ == "__main__":
    main()