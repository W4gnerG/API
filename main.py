import requests
import json
import time

print("Iniciando script...")

try:
    f = open("config.txt", "r")
    if f.mode == "r":
        token = f.read()
    f.close()
except:
    f = open("config.txt", "w+")
    f.close()
    print("Error reading or creating config file")

pairs = ["BRLBTC", "BRLETH", "BRLLTC", "BRLBCH", "BRLXRP"]
lastPrice = [0, 1, 2, 3, 4]


def ticker(pair):

    url = "https://api.bitcointrade.com.br/v2/public/"+pair+"/ticker"

    payload = {}
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    ticker = json.loads(response.text)

    if pair == "BRLBTC":
        lastPrice[0] = ticker['data']['last']
    elif (pair == "BRLETH"):
        lastPrice[1] = ticker['data']['last']
    elif (pair == "BRLLTC"):
        lastPrice[2] = ticker['data']['last']
    elif (pair == "BRLBCH"):
        lastPrice[3] = ticker['data']['last']
    elif (pair == "BRLXRP"):
        lastPrice[4] = ticker['data']['last']

    return lastPrice


while True:

    # Cotações
    for value in pairs:
        ticker(value)
        print(json.dumps(lastPrice[0], indent=4, sort_keys=False))

    # Saldo da Carteira
    url = "https://api.bitcointrade.com.br/v3/wallets/balance"

    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': token
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    balance = json.loads(response.text)

    print(json.dumps(balance, indent=4, sort_keys=False))

    url = "https://api.bitcointrade.com.br/v2/market?pair=BRLBTC"

    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'Authorization': token
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    time.sleep(1)
