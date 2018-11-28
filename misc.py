import random
import requests
import yaml

config = yaml.load(open('config.yaml'))

def excuse():
    message = random.choice(config['misc']['excuses'])

    return message


def dolar():
    url = 'https://www.bancogalicia.com/cotizacion/cotizar?currencyId=02&quoteType=SU&quoteId=999'

    r = requests.get(url)
    buy = r.json()['buy']
    sell = r.json()['sell']

    message = f"```\nBuy: {buy} ARS\nSell: {sell} ARS\n```"

    return message