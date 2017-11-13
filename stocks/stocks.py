import requests, json

class Stock:
    def __init__(self, name=""):
        self.name = name.upper()
        self.url = "https://query2.finance.yahoo.com/v10/finance/quoteSummary/"+ self.name +"?modules=financialData&output=json"
        self.resp_dict = self.refresh()

    def refresh(self):
            resp = requests.get(self.url).text
            resp_dict = json.loads(resp)
            return resp_dict

    def get_name(self):
        return self.name

    def get_price(self):
        return float(self.resp_dict['quoteSummary']['result'][0]['financialData']['currentPrice']['fmt'].replace(',',''))

    def get_percent_differnce(self, data_type):
        if data_type.upper() is "DAY":
            return
        if data_type.upper() is "WEEK":
            print("WEEK not supported")
            return
        if data_type.upper() is "MONTH":
            print("MONTH not supported")
            return
        if data_type.upper() is "YEAR":
            print("YEAR not supported")
            return
