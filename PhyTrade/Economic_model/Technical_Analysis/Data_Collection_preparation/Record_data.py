import pandas as pd

df = pd.DataFrame([['a', 'b'], ['c', 'd']],
                   index=['row 1', 'row 2'],
                   columns=['col 1', 'col 2'])


# df.to_json(orient='split')
# '{"columns":["col 1","col 2"],
#   "index":["row 1","row 2"],
#   "data":[["a","b"],["c","d"]]}'