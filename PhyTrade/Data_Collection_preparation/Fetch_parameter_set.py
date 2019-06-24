import json
import os


def fetch_parameter_set(ticker, run_count):

    path = r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Python\Steffegium\Data\EVOA_results\Parameter_sets\Run_##_**.json"
    path = path.replace('\\', '/').replace('##', str(run_count)).replace('**', ticker)

    # ---> Check if generated path data exists in database
    if os.path.exists(path):
        return json.load(open(path))
    else:
        # print("Run_"+ticker+"_"+str(run_count), "parameter set does not exist")
        return None


def fetch_parameter_sets(tickers, run_count):
    parameter_sets = []
    traded_tickers = []
    for ticker in tickers:
        param_set = fetch_parameter_set(ticker, run_count)
        if param_set is not None:
            traded_tickers.append(ticker)
            parameter_sets.append(param_set)

    assert(len(traded_tickers) == len(parameter_sets))
    return traded_tickers, parameter_sets
