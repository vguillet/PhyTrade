
##################################################################################################################
"""
Used to record spline generated - Format: ["Date", "trade_spline", "trade_signal"]
"""

# Built-in/Generic Imports
import os.path

# Libs
import pandas as pd

# Own modules
from PhyTrade.Tools.INDIVIDUAL_gen import Individual

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

##################################################################################################################


def record_splines(parameter_set, data_slice, ticker, spline_type=None):
    """
    Used to record a collection of spines

    :param parameter_set: Parameter set dictionary to be used fro spline generation
    :param data_slice: Data_slice type object
    :param ticker: Ticker of company
    :param spline_type: String used to specify save folder (folder need to be already present)

    :return: CSV of splines indexed by date
    """

    individual = Individual(ticker=ticker, parameter_set=parameter_set)
    individual.gen_economic_model(data_slice)

    spline_df = pd.DataFrame(columns=["Date", "trade_spline", "trade_signal"])

    spline_df["Date"] = data_slice.data[data_slice.start_index:data_slice.stop_index]["Date"]
    spline_df["trade_spline"] = individual.trade_spline
    spline_df["trade_signal"] = individual.trade_signal

    # ---> Save spline to csv file
    if spline_type is None:
        path = r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Python\Steffegium\Data\Splines".replace('\\', '/')
    else:
        path = r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Python\Steffegium\Data\**".\
            replace('\\', '/').replace('**', spline_type)

    full_file_name = path + '/' + ticker + "_splines"

    if os.path.isfile(full_file_name):
        new_df = pd.concat([pd.read_csv(full_file_name, index_col=0), spline_df])
        new_df.to_csv(full_file_name)

    else:
        spline_df.to_csv(full_file_name)
