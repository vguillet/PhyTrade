from PhyTrade.Settings.SETTINGS import SETTINGS


class MARKET_tools:
    def calc_transaction_cost(self, asset_count):
        settings = SETTINGS()
        settings.market_settings.gen_market_settings()

        transaction_cost = asset_count*settings.market_settings.transaction_cost_per_share
        if transaction_cost < settings.market_settings.min_transaction_cost:
            transaction_cost = settings.market_settings.min_transaction_cost

        return transaction_cost
