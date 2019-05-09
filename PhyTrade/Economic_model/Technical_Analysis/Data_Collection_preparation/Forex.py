from forex_python.converter import CurrencyRates
import pandas as pd

c = CurrencyRates()

# print(c.get_rates("USD"))


datelst = pd.date_range(pd.datetime.today(), periods=100).tolist()

rateslst = []

for date in datelst:
    rateslst.append(c.get_rate('USD', 'INR', date))

print(rateslst)
