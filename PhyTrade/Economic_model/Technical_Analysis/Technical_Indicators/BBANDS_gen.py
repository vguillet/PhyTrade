# Compute the Bollinger Bands
def BBANDS_gen(data, window=n):
 MA = data.Close.rolling(window=n).mean()
 SD = data.Close.rolling(window=n).std()
 data['UpperBB'] = MA + (2 * SD)
 data['LowerBB'] = MA - (2 * SD)
 return data