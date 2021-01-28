
##################################################################################################################
"""
This function is used to collect the parameter set dictionaries
"""

# Built-in/Generic Imports
import json

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '20/09/2019'

##################################################################################################################


def gen_parameters_json(run_label, ticker, parameter_dictionary):
    """
    Used to record parameter set dictionaries as json files

    :param run_label: Run label to be used in file name
    :param ticker: Ticker of parameter set
    :param parameter_dictionary: Parameter set dictionary
    """
    path = r"Data/EVOA_results/Parameter_sets".replace('\\', '/')
    file_name = path + '/' + run_label + "_" + ticker + ".json"

    with open(file_name, 'w') as fout:
        json.dump(parameter_dictionary, fout, indent=4)
    print("Parameters recorded to ", file_name, " successfully\n")
    return
