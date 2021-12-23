import requests
import json
from config import available, USE_API


class APIException(Exception):
    pass


class ExchangeRates:
    @staticmethod
    def get_price(quote: str, base: str, amount_str: str):
        if quote == base:
            raise APIException(f'Указаны одинаковые имена валют <{quote}>!')

        try:
            quote_code = available[quote]
        except KeyError:
            raise APIException(f'Валюта <{quote}> не обработана!\n/values - список доступных валют')

        try:
            base_code = available[base]
        except KeyError:
            raise APIException(f'Валюта <{base}> не обработана!\n/values - список доступных валют')

        try:
            amount = float(amount_str)
        except ValueError:
            raise APIException(f'Количество <{amount_str}> не является числом!')

        r = requests.get(f'https://www.alphavantage.co/query?function=CURRENCY_EXCHANGE_RATE&\
from_currency={quote_code}&to_currency={base_code}&apikey={USE_API}')

        price = json.loads(r.content)['Realtime Currency Exchange Rate']['5. Exchange Rate']
        total = float(price) * amount

        return total
