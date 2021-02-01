
##################################################################################################################
"""
Used to fetch a formatted list of the parameter sets available per ticker
"""

# Built-in/Generic Imports
from toolz import interleave
import os

# Libs
import pandas as pd

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

##################################################################################################################


def fetch_parameter_set_labels_df(prints=True):
    paths = {"(Short term)": r"Data/EVOA_results/Parameter_sets/Short_term",
             "(Long term)": r"Data/EVOA_results/Parameter_sets/Long_term"}
    ps_df_path = ["--> Short term:", "--> Long term:"]
    ps_df = []

    for path in paths.keys():
        tickers = []
        run_counts = []

        ps = [name for name in os.listdir(paths[path]) if os.path.isfile(os.path.join(paths[path], name))]

        for ps_instance in ps:
            run_counts.append(ps_instance[4:6])
            tickers.append(ps_instance[7:-5])

        cm_init = [[0]*len(set(run_counts))]*len(set(tickers))

        df = pd.DataFrame(cm_init, columns=set(run_counts), index=set(tickers))
        # df.index.name = "Tickers"

        for ps_instance in range(len(ps)):
            df.at[tickers[ps_instance], run_counts[ps_instance]] += 1

        # df = df.add_suffix(" " + path)
        ps_df.append(df)

    # ps_df = pd.concat(ps_df, axis=1)
    # print(ps_df, "\n")

    if prints:
        print("\n")
        for df in range(len(ps_df)):
            print(ps_df_path[df] + "\n", ps_df[df], "\n\n")

    return ps_df