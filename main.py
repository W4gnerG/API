import requests
import json
import time
import semantic

pairs = ["BRLBTC", "BRLETH", "BRLLTC", "BRLBCH", "BRLXRP"]


def readConfig():
    try:
        f = open("config.txt", "r")
        if f.mode == "r":
            token = f.read()
        f.close()
    except:
        f = open("config.txt", "w+")
        f.close()
        print("Error reading or creating config file")

    return token


def ticker(pair):

    url = "https://api.bitcointrade.com.br/v2/public/"+pair+"/ticker"

    payload = {}
    headers = {
        'Content-Type': 'application/json'
    }

    response = requests.request("GET", url, headers=headers, data=payload)
    ticker = json.loads(response.text)
    lastPrice = [0, 1, 2, 3, 4]

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


def main():

    token = readConfig()
    while True:

        # Cotações
        for value in pairs:
            ticker(value)
            #print(json.dumps(lastPrice[0], indent=4, sort_keys=False))

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

        # Book Orders
        url = "https://api.bitcointrade.com.br/v3/market?pair=BRLBTC"

        payload = {}
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': token
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        book = json.loads(response.text)

        #print(json.dumps(book, indent=4, sort_keys=False))

        time.sleep(1)


if __name__ == "__main__":
    main()
