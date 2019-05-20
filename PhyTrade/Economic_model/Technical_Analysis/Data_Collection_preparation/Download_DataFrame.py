from PhyTrade.Economic_model.Technical_Analysis.Data_Collection_preparation.Yahoo import pull_yahoo_data


def save_df_to_csv(df, file_name):
    """
    Save Pandas dataframe to:
     C:\\\Users\\\Victor Guillet\\\Google Drive\\\\2-Programing\\\Repos\\\Python\\\Steffegium\\\Research\\\Data

    :param df: Pandas dataframe
    :param file_name: Desired file name .csv
    """

    path = r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Python\Steffegium\Research\Data".replace('\\', '/')
    full_file_name = path + '/' + file_name
    df.to_csv(full_file_name)

    return


if __name__ == "__main__":
    ticker = "AAPL"

    data = pull_yahoo_data(ticker)
    # data = pull_quandl_data(ticker)

    file_name = ticker+"_Yahoo_data.csv"
    save_df_to_csv(data, file_name)
