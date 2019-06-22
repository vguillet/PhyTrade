import json
import os


def fetch_parameter_set(ticker, run_count):
    path = r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Python\Steffegium\Data\EVOA_results\Parameter_sets\Run_##_**.json"
    path = path.replace('\\', '/').replace('##', str(run_count)).replace('**', ticker)

    # ---> Check if generated path data exists in database
    if os.path.exists(path):
        return json.load(open(path))
    else:
        print("Parameter set does not exist")
