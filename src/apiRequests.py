import json
import requests
from os import path

token = ""


def ReadConfig():
    try:
        f = open("../config.json", "r")
        if f.mode == "r":
            global token
            token = json.loads(f.read())
            token = token['token']
        f.close()
    except:
        if path.exists("../config.json") is True:
            print("Error reading config file")
        else:
            f = open("config.json", "w+")
            f.close()
            print("Error creating config file")


def GetPrice(pair):
    status_code = 0
    while (status_code != 200):
        url = "https://api.bitcointrade.com.br/v3/public/" + pair + "/ticker"

        payload = {}
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        status_code = response.status_code

    return json.loads(response.text)['data']


def GetBalance():
    url = "https://api.bitcointrade.com.br/v3/wallets/balance"
    global token
    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': token
    }

    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        return json.loads(response.text)['data']
    except:
        return ''


def GetBookOrders():
    url = "https://api.bitcointrade.com.br/v3/market?pair=BRLBTC"

    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': token
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return json.loads(response.text)
