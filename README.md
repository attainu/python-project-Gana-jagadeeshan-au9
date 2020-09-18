
# What is Bitcoin?

Bitcoin offers an efficient means of transferring money over the internet and is controlled by a decentralized network with a transparent set of rules, thus presenting an alternative to central bank-controlled fiat money.

## Advantage of Bitcoin:
```
By using a cryptocurrency, users are able to exchange value digitally without third party oversight.
```

# Problem Faced by Users:
The main Issue with Bitcoin is that it is "FICKLE THING" and its value changes every minute.

## BITCOIN-ALERT PROJECT:
This Project consistes of a "Bitcoin-Notification Messaging Service" that can be used to send Real-Time Bitcoin Prices to target Messaging Service like Telegram,Twitter,Phone SMS and Push Notification(IFTTT App).

# Installation Guide:
install bitcoin price notifier package using pip.
```
pip install Bitcoinprice-notifications
```
For Help Menu
```
Bitcoin-Price-Notification --help
```

you will see a Response like this

```
usage: 
    Usage: This app gives the price of 1 BTC in INR. Destination(-d) must be provided. To recive notification
    from IFTTT install IFTTT mobile app. To recive notifications on Telegram install Telegram app and join this channel 
    https://t.me/testbitcoinprice.  Prerequisite : MUST HAVE A IFTTT APP AND TELEGRAM APP.
 INSTALLED TO RECIVE NOTIFICATION 
    ALSO MUST JOIN THE TELEGRAM Bit_Coin CHANNEL TO RECIVE MESSAGES. PRESS Ctrl+C to terminate the app.
Bitcoin price Notification

optional arguments:

                   ('''-h, --help           -- Help with this Application
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
```
to run the app, type the following command
```
python3 bitcoin.py -a 100000 -t 1 -l 3 -d telegram
```
* -a alertPrice
* -t timeFrequency
* -l logLength
* -d destination_app
* -c currency 

#AUTHOR: GANAPATHY J