import time
from datetime import datetime
import apiRequests as api

lastPrice = []
pairs = ['BRLBTC', 'BRLETH', 'BRLLTC', 'BRLBCH', 'BRLXRP']


def main():
    api.ReadConfig()
    try:
        while True:

            # Últimos preços
            lastPrice = []

            for value in pairs:
                lastPrice.append(api.GetPrice(value))

            # Saldo da Carteira
            balance = api.GetBalance()

            balanceBRL = balance[0]['available_amount']
            balanceBTC = balance[1]['available_amount']
            balanceETH = balance[2]['available_amount']
            balanceLTC = balance[3]['available_amount']
            balanceBCH = balance[4]['available_amount']
            balanceXRP = balance[5]['available_amount']
            # balanceEOS = balance[6]['available_amount']

            totalBalance = balanceBRL + (
                balanceBTC * lastPrice[0]['sell']) + (
                balanceETH * lastPrice[1]['sell']) + (
                balanceLTC * lastPrice[2]['sell']) + (
                balanceBCH * lastPrice[3]['sell']) + (
                balanceXRP * lastPrice[4]['sell'])

            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            message = '> Total Balance is: R${:.2f}'
            print(dt_string, str(message.format(totalBalance)).replace(".", ","))

            # Livro de orfertas
            bookOrders = api.GetBookOrders()

            time.sleep(10)

    except (KeyboardInterrupt):
        print(' Encerrando...')
    except:
        print('Error')


if __name__ == "__main__":
    main()
