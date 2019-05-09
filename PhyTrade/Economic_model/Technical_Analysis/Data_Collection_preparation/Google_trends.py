from pytrends.request import TrendReq


def pull_google_trends_data(keyword, cat='', geo='', timeframe='', gprop=''):
    pytrend_obj = TrendReq()
    pytrend_obj.build_payload(keyword, cat=cat, geo=geo, timeframe=timeframe, gprop=gprop)
    interest_over_time_df = pytrend_obj.interest_over_time()
    data = interest_over_time_df[keyword]

    return data
