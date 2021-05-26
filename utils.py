import requests
import json
from config import currencies


class ConversionException(Exception):
    pass


class Converter:
    @staticmethod
    def convert(currency1, currency2, amount):
        if currency1 == currency2:
            raise ConversionException(f'Вы ввели одинаковые валюты ({currency1}), введите разные')

        try:
            cur1_ticker = currencies[currency1]
        except KeyError:
            raise ConversionException(f'Не удалось обработать валюту {currency1}')

        try:
            cur2_ticker = currencies[currency2]
        except KeyError:
            raise ConversionException(f'Не удалось обработать валюту {currency2}')

        try:
            amount = float(amount)
        except ValueError:
            raise ConversionException(f'Не удалось обработать количество "{amount}"')

        r = requests.get(f'http://api.exchangeratesapi.io/v1/latest?access_key=395d5d85b3074113b729950b84144d7e')
        currency1_in_euro = json.loads(r.content)['rates'][cur1_ticker]  # стоимтость одного евро в валюте
        currency2_in_euro = json.loads(r.content)['rates'][cur2_ticker]
        res = float(currency2_in_euro / currency1_in_euro) * int(amount)
        return round(res, 4)
