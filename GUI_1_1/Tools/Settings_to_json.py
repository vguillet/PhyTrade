
##################################################################################################################
"""

"""

# Built-in/Generic Imports
import datetime
import json

# Libs

# Own modules

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = ''

##################################################################################################################


def record_settings(dictionary, setting_category, name=None):
    path = r"C:\Users\Victor Guillet\Google Drive\Computer science\2-Programing\Repos\Python\Steffegium\Data\Settings"

    if name is not None:
        file_name = path + '/' + setting_category + '/' + name + str(datetime.datetime.now().date()) + ".json"

    else:
        file_name = path + '/' + setting_category + '/' + str(datetime.datetime.now().date()) + ".json"

    with open(file_name, 'w') as fout:
        json.dump(dictionary, fout, indent=4)
