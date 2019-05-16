import quandl


def pull_quandl_data(ticker):
    """
    Download financial data from Quandl for a specific ticker

    :param ticker: Desired ticker
    :return: Pandas dataframe
    """
    quandl.ApiConfig.api_key = 'xNpTC2yJ-16KX_or92WR'   # API key for Quandl authentication
    data = quandl.get(ticker)                           # Fetch data matching selected ticker
    # data = data.iloc[::-1]                            # Reindex data ti invert df
    print("--Quandl data pulled successfully--")
    print("Number of points pulled:", len(data))
    print("-----------------------------------")

    return data
