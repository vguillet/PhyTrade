

class GENERAL_tools:
    @staticmethod
    def calc_nested_dic_item_count(dictionary):
        count = 0
        for key in dictionary:
            if type(dictionary[key]) is dict:
                count += GENERAL_tools().calc_nested_dic_item_count(dictionary[key])
            else:
                if type(dictionary[key]) is list:
                    count += len(dictionary[key])
                elif type(dictionary[key]) is int or type(dictionary[key]) is float or type(dictionary[key]) is bool:
                    count += 1
                else:
                    print("ERROR", type(dictionary[key]))
        return count
