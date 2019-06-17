from PhyTrade.Economic_model.Technical_Analysis.Technical_Indicators.ABSTRACT_indicator import ABSTRACT_indicator


class EVM(ABSTRACT_indicator):
    def __init__(self):

        def EVM(data, ndays):
         dm = ((data['High'] + data['Low'])/2) - ((data['High'].shift(1) + data['Low'].shift(1))/2)
         br = (data['Volume'] / 100000000) / ((data['High'] - data['Low']))
         EVM = dm / br
         EVM_MA = pd.Series(pd.rolling_mean(EVM, ndays), name = 'EVM')
         data = data.join(EVM_MA)