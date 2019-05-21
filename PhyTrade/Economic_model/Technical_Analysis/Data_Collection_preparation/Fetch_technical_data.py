from PhyTrade.Economic_model.Technical_Analysis.Data_Collection_preparation.Yahoo import pull_yahoo_data
import pandas
import os


def fetch_technical_data(ticker):
    path = r"Research\Data\**_Yahoo_data.csv".replace('\\', '/').replace('**', ticker)

    # ---> Check if generated path data exists in database
    if os.path.exists(path):
        data = pandas.read_csv(path)

    # --> Else, download data
    else:
        # ---> Pull data from Yahoo
        data = pull_yahoo_data(ticker)
        file_name = ticker + "_Yahoo_data.csv"

        # ---> Save data to csv file
        path = r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Python\Steffegium\Research\Data".replace('\\', '/')
        full_file_name = path + '/' + file_name

        data.to_csv(full_file_name)

    return data
