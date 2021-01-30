
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

    :param parameter_set: Parameter set dictionary to be used for spline generation
    :param data_slice: Data_slice type object
    :param ticker: Ticker of company
    :param spline_type: String used to specify save folder (folder need to be already present)

    :return: CSV of splines indexed by date
    """

    individual = Individual(parameter_set=parameter_set)
    individual.gen_economic_model(data_slice)

    spline_df = pd.DataFrame(columns=["Date", "trade_spline", "trade_signal"])

    spline_df["Date"] = data_slice.data[data_slice.subslice_start_index:data_slice.subslice_stop_index]["Date"]
    spline_df["trade_spline"] = individual.analysis.trade_spline
    spline_df["trade_signal"] = individual.analysis.trade_signal

    # ---> Save spline to csv file
    if spline_type is None:
        path = r"Data\Splines".replace('\\', '/')
    else:
        path = r"Data\**".\
            replace('\\', '/').replace('**', spline_type)

    full_file_name = path + '/' + ticker + "_splines.csv"

    if os.path.isfile(full_file_name):
        new_df = pd.concat([pd.read_csv(full_file_name, index_col=0), spline_df])
        new_df.to_csv(full_file_name)

    else:
        spline_df.to_csv(full_file_name)
