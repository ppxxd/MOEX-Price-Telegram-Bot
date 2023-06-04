import requests
from bs4 import BeautifulSoup


class CurrencyInfo:
    moex_dict = {"USD": 'USD000UTSTOM', #Американский доллар
                 "EUR": 'EUR_RUB__TOM', #Евро
                 "CNY": 'CNYRUB_TOM', #Китайский юань
                 "HKD": 'HKDRUB_TOM', #Гонконгский доллар
                 "TRY": 'TRYRUB_TOM', #Турецкая лира
                 "BYN": 'BYNRUB_TOM', #Белорусский рубль
                 "KZT": 'KZTRUB_TOM', #Казахстанский тенге
                 "AMD": 'AMDRUB_TOM'} #Армянский драм


    def __init__(self, message):
        self.message = message
        self.headers = {"User-Agent": "User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                                      "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.6.1 Safari/605.1.15"}
        self.currency = None
        self.tickerlink = None
        self.price = None
        self.change = None

    def info_moex(self):
        url = f'https://iss.moex.com/iss/engines/currency/markets/selt/securities/' \
                  f'{self.moex_dict.get(self.message)}.xml'
        pages = requests.get(url, timeout=10, headers=self.headers)
        soup = BeautifulSoup(pages.text, 'xml')
        if self.moex_dict.get(self.message):
            info = ((soup.find(id="marketdata")).find_all('row'))
            lasts = [i.get('LAST') for i in info if len(i.get('LAST')) != 0]
            opens = [i.get('OPEN') for i in info if len(i.get('OPEN')) != 0]
            try:
                currency = self.message
                tickerlink = f'https://www.moex.com/en/issue/{self.moex_dict.get(self.message)}/CETS'
                price = float(lasts[0])
                change = round(price * 100 / (float(opens[0])) - 100, 2)
            except (IndexError, TypeError, ValueError):
                return print("Error")
        else:
            currency, tickerlink, price, change = None, None, None, None
        return self.set_info(currency, tickerlink, price, change)

    def set_info(self, currency, tickerlink, price, change):
        if currency:
            self.currency = f"{currency} to RUB - <a href='{tickerlink}'>open on MOEX</a>\n"
            self.price = f"\nPrice: <b>{price}</b> RUB" if price else 0
            self.change = f"\nToday's change: <b>{change}</b>%"

    def get_info(self):
        self.info_moex()
        if self.price:
            return f"{self.currency} {self.price} {self.change}"
        else:
            return f"{self.message} - ticker not found or the server is not responsing."
