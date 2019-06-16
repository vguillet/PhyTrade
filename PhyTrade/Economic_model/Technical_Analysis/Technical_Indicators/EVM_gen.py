def EVM(data, ndays):
 dm = ((data['High'] + data['Low'])/2) - ((data['High'].shift(1) + data['Low'].shift(1))/2)
 br = (data['Volume'] / 100000000) / ((data['High'] - data['Low']))
 EVM = dm / br
 EVM_MA = pd.Series(pd.rolling_mean(EVM, ndays), name = 'EVM')
 data = data.join(EVM_MA)