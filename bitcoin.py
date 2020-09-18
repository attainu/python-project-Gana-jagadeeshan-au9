
import time
import argparse
import requests
import json
from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
from datetime import datetime
import getopt
import sys

BITCOIN_API_URL = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'
IFTTT_WEBHOOKS_URL = "https://maker.ifttt.com/trigger/{}/with/key/bwBBdvI5locB8l3AqREhx9"


def get_latest_bitcoin_price():
    # coinmarketcap api url
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    parameters = {"start": "1", "limit": "5000", "convert": "INR"}

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
    print("BTC Price", float(data['data'][0]['quote']['INR']['price']))
    return float(data['data'][0]['quote']['INR']['price'])


def post_ifttt_webhook(event, data):
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


def update_Price_History(bitcoin_history, logLength, event):
    # Once we have 5 items in our bitcoin_history send an update
    if len(bitcoin_history) == logLength:
        post_ifttt_webhook(event, {"value1": "Bit_Coin_Price_History",
                                   "value2": format_bitcoin_history(bitcoin_history)})
        # Reset the history
        bitcoin_history = []


def main(alertPrice, timFrequency, logLength, destination_app, currency):
    bitcoin_history = []
    while True:
        price = get_latest_bitcoin_price()
        price = round(price, 2)
        date = datetime.now()
        bitcoin_history.append({'date': date, 'price': price})

        # Send an emergency notification
        if price > alertPrice:
            if destination_app == "Telegram":
                print("Sending notification to telegram")
                post_ifttt_webhook('Bit_Coin_Telegram', {
                                   "value1": "Bit_Coin_Price_Above_Threshold", "value2": price})
                update_Price_History(
                    bitcoin_history, logLength, "Bit_Coin_Telegram")
            elif destination_app == "Twitter":
                post_ifttt_webhook('Bit_Coin_Twitter', {
                                   "value1": "Bit_Coin_Price_Above_Threshold", "value2": price})
                update_Price_History(
                    bitcoin_history, logLength, "Bit_Coin_Twitter")

        # Send a Telegram notification
        time.sleep(timFrequency)


if __name__ == '__main__':
    # Remove 1st argument from the
    # list of command line arguments
    argumentList = sys.argv[1:]
    print("=================================")
    print("WELCOME TO BITCOIN PRICE NOTIFIER")
    print("=================================")
    # Options
    options = "ha:t:l:d:c:"
    # print("Argument list ==> ",argumentList)
    # Long options
    long_options = ["help", "alertPrice =", "timeFrequency =",
                    "logLength =", "destination_app =", "currency ="]
    AlertPrice = 10000
    TimeFrequency = 1*60
    Log_Length = 2
    Destination_App = "Telegram"
    Currency = "INR"
    try:
        # Parsing argument
        arguments, values = getopt.getopt(argumentList, options, long_options)
        # print("Arg,Value====>",arguments,values)
        print(getopt.getopt(argumentList, options, long_options))
        # checking each argument
        for currentArgument, currentValue in arguments:

            if currentArgument in ("-h", "--help"):
                print('''-h, --help           -- Help with this Application
                    -a alertPrice
                                        The price of 1 bitcoin when an emergency alert will be
                                        sent. Default is 10000 USD
                    -t timeFrequency
                                        The Frequency at which the the Bitcoin value is going
                                        to be Fetched from Server in minutes. Default 1 min
                    -l logLength
                                        The number of Entries you would like to Send,the
                                        default is #2 Entries
                    -d destination_app
                                        The Messaging Service Destiation
                                        1. Telegram
                                        2. Twitter
                                        Default : Telegram

                    -c currency        INR
                ''')

            else:
                if currentArgument in ("-a", "--alertPrice"):
                    AlertPrice = int(currentValue)
                    print("Displaying AlertPrice: ", AlertPrice)
                elif currentArgument in ("-t", "--timeFrequency"):
                    TimeFrequency = int(currentValue)
                    print(("TimeFrequency (% s)") % (currentValue))
                elif currentArgument in ("-l", "--logLength"):
                    Log_Length = int(currentValue)
                    print(("Log length (% s)") % (currentValue))
                elif currentArgument in ("-d", "--destination_app"):
                    Destination_App = currentValue
                    print(("TimeFrequency (% s)") % (currentValue))
                elif currentArgument in ("-c", "--currency"):
                    Currency = currentValue
                    print(("Log length (% s)") % (currentValue))

    except getopt.error as err:
        # output error, and return with an error code
        print(str(err))

    main(AlertPrice, TimeFrequency, Log_Length, Destination_App, Currency)
