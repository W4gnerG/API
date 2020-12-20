import json
import requests
from os import path, stat

token = ""


def ReadConfig():
    try:
        if path.exists("./config.json") is True:
            f = open("./config.json", "r")
            if stat("config.json").st_size > 0:
                global token
                dados = json.loads(f.read())
                token = dados['token']
            else:
                print("Insert the token inside config file")
                exit()
            f.close()
        else:
            f = open("config.json", "w+")
            print("Created config file")
            exit()
    except:
        print("There has ben an error reading the file")
        exit()


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
