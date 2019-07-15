from PhyTrade.Tools.INDIVIDUAL_gen import Individual
import pandas as pd


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

    index = data_slice.data[data_slice.default_start_index:data_slice.default_end_index]["Date"]
    spline_df = pd.DataFrame(index=index, columns=["trade_spline", "trade_signal"])

    # TODO: Fixed length index error

    spline_df["trade_spline"] = individual.trade_spline
    spline_df["trade_signal"] = individual.trade_signal

    # ---> Save spline to csv file
    if spline_type is None:
        path = r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Python\Steffegium\Data\Splines".replace(
            '\\', '/')
    else:
        path = r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Python\Steffegium\Data\Metalabeling_results\**".\
            replace('\\', '/').replace('**', spline_type)

    full_file_name = path + '/' + ticker + "_splines_" + data_slice.default_start_date + " - " + data_slice.default_end_date
    spline_df.to_csv(full_file_name)

