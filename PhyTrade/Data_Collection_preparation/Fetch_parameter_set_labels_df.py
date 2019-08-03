import pandas as pd
from toolz import interleave

import os


def fetch_parameter_set_labels_df():
    path_short_term = r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Python\Steffegium\Data\EVOA_results\Parameter_sets\Short_term"
    path_long_term = r"C:\Users\Victor Guillet\Google Drive\2-Programing\Repos\Python\Steffegium\Data\EVOA_results\Parameter_sets\Long_term"

    paths = {"(Short term)": path_short_term, "(Long term)": path_long_term}
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

    print("\n")
    for df in range(len(ps_df)):
        print(ps_df_path[df] + "\n", ps_df[df], "\n\n")
