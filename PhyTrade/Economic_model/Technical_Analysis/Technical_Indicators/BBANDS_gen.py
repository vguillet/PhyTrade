from PhyTrade.Economic_model.Technical_Analysis.Technical_Indicators.ABSTRACT_indicator import ABSTRACT_indicator
# Compute the Bollinger Bands
def BBANDS_gen(data, window=n):
 MA = data.Close.rolling(window=n).mean()
 SD = data.Close.rolling(window=n).std()
 data['UpperBB'] = MA + (2 * SD)
 data['LowerBB'] = MA - (2 * SD)
 return data