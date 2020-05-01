import requests
import json
import time

token = ''
lastPrice = []
pairs = ['BRLBTC', 'BRLETH', 'BRLLTC', 'BRLBCH', 'BRLXRP']


def readConfig():

    try:
        f = open("config.json", "r")
        if f.mode == "r":
            global token
            token = json.loads(f.read())
            token = token['token']
        f.close()
    except:
        f = open("config.json", "w+")
        f.close()
        print("Error reading or creating config file")


def getPrice(pair):
    status_code = 0
    while(status_code != 200):
        url = "https://api.bitcointrade.com.br/v3/public/"+pair+"/ticker"

        payload = {}
        headers = {
            'Content-Type': 'application/json'
        }

        response = requests.request("GET", url, headers=headers, data=payload)
        status_code = response.status_code

    return json.loads(response.text)['data']


def getBalance():
    url = "https://api.bitcointrade.com.br/v3/wallets/balance"
    global token
    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'x-api-key':  token
    }

    try:
        response = requests.request("GET", url, headers=headers, data=payload)
        return json.loads(response.text)['data']
    except:
        return ''


def getBookOrders():

    url = "https://api.bitcointrade.com.br/v3/market?pair=BRLBTC"

    payload = {}
    headers = {
        'Content-Type': 'application/json',
        'x-api-key': token
    }

    response = requests.request("GET", url, headers=headers, data=payload)

    return json.loads(response.text)


def main():
    readConfig()
    try:

        while True:

            lastPrice = []

            for value in pairs:
                lastPrice.append(getPrice(value))

            # Saldo da Carteira
            balance = getBalance()

            balanceBRL = balance[0]['available_amount']
            balanceBTC = balance[2]['available_amount']
            balanceETH = balance[3]['available_amount']
            balanceLTC = balance[4]['available_amount']
            balanceBCH = balance[5]['available_amount']
            balanceXRP = balance[6]['available_amount']

            totalBalance = balanceBRL + (
                balanceBTC * lastPrice[0]['sell']) + (
                    balanceETH * lastPrice[1]['sell']) + (
                        balanceLTC * lastPrice[2]['sell']) + (
                            balanceBCH * lastPrice[3]['sell']) + (
                                balanceXRP * lastPrice[4]['sell'])

            message = '> Total Balance is: R${:.2f}'
            print(message.format(totalBalance))

            # Livro de orfertas
            bookOrders = getBookOrders()

            time.sleep(10)
    except (KeyboardInterrupt):
        print(' Encerrando...')
    except:
        print('Error')
        


if __name__ == "__main__":
    main()
