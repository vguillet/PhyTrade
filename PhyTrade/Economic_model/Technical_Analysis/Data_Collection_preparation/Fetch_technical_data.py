from PhyTrade.Economic_model.Technical_Analysis.Data_Collection_preparation.Yahoo import pull_yahoo_data
import pandas
import os


def fetch_technical_data(ticker):
    path = r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Python\Steffegium\Data\Technical_data\**_Yahoo_data.csv".replace('\\', '/').replace('**', ticker)

    # ---> Check if generated path data exists in database
    if os.path.exists(path):
        data = pandas.read_csv(path)

    # --> Else, download data
    else:
        # ---> Pull data from Yahoo
        data = pull_yahoo_data(ticker)
        file_name = ticker + "_Yahoo_data.csv"

        # ------------------ Fill in missing values (weekends)
        idx = pandas.date_range(data.index[0], data.index[-1])
        data = data.reindex(idx)
        data = data.fillna(method='ffill')

        data = data.reset_index()

        # ---> Save data to csv file
        path = r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Python\Steffegium\Data\Technical_data".replace('\\', '/')
        full_file_name = path + '/' + file_name

        data.to_csv(full_file_name)

    return data
