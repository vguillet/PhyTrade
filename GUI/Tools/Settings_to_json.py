
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


def record_settings(dictionary, setting_category, name):
    path = r"Settings".replace('\\', '/')

    print("----------------> Record settings", setting_category)
    if setting_category == "Current_settings":
        file_name = path + '/' + setting_category + '/' + name + ".json"

    elif name[-1] != "_":
        file_name = path + '/' + setting_category + '/' + name + '_' + datetime.date.today().strftime("%Y-%m-%d").replace(" ", "_") + ".json"

    else:
        file_name = path + '/' + setting_category + '/' + name  + datetime.date.today().strftime("%Y-%m-%d") + ".json"

    with open(file_name, 'w') as fout:
        json.dump(dictionary, fout, indent=4)
