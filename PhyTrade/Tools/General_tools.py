
################################################################################################################
"""
Contains general python tools
"""

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

################################################################################################################


class General_tools:
    @staticmethod
    def calc_nested_dic_item_count(dictionary, blacklist):
        count = 0
        for key in dictionary:
            if key in blacklist:
                continue
            elif type(dictionary[key]) is dict:
                count += General_tools().calc_nested_dic_item_count(dictionary[key], blacklist)
            else:
                if type(dictionary[key]) is list:
                    count += len(dictionary[key])
                elif type(dictionary[key]) is int or type(dictionary[key]) is float or type(dictionary[key]) is bool:
                    count += 1
                else:
                    print("ERROR", type(dictionary[key]), "not accounted for")
        return count
