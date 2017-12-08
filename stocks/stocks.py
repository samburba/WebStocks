import requests, json, datetime
from datetime import timedelta
import pandas_datareader as pdr

class Stock:
    def __init__(self, name=""):
        self.name = name.upper()
        self.url = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/"+ self.name +"?modules=financialData&output=json"
        self.year = datetime.datetime.now().year
        try:
            self.hist_prices = pdr.DataReader(self.name, 'yahoo', self.year)['Close']
        except:
            self.hist_prices = -1
        self.resp_dict = self.refresh()

    def refresh(self):
            resp = requests.get(self.url).text
            resp_dict = json.loads(resp)
            self.year = datetime.datetime.now().year
            try:
                self.hist_prices = pdr.DataReader(self.name, 'yahoo', self.year)['Close']
            except:
                self.hist_prices = -1
            return resp_dict

    def get_name(self):
        return self.name

    def get_price(self):
        return float(self.resp_dict['quoteSummary']['result'][0]['financialData']['currentPrice']['fmt'].replace(',',''))

    def get_percent_difference(self):
        if self.hist_prices is -1:
            return "Oops, something went wrong."
        return round((100 * (self.get_price() - self.hist_prices[-2]) / self.hist_prices[-2]), 2)

    def get_week_prices(self):
        end = datetime.datetime.today()
        start = end - timedelta(weeks=1)
        to_return = "Error"
        try:
            to_return = pdr.DataReader(self.name, "yahoo", start, end)
        except:
            return to_return
        return to_return
