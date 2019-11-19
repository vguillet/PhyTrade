import pandas


def fetch_company_tickers(start_ind=0, stop_ind=10):
    path = r"Data\Company_data\companylist.csv".replace('\\', '/')
    data = pandas.read_csv(path)
    return list(data["Symbol"][start_ind:stop_ind])
