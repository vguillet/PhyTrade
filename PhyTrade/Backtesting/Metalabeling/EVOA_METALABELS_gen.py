from PhyTrade.Signal_optimisation.EVOA_optimisation.EVO_algo_4 import EVOA_optimiser
from PhyTrade.Data_Collection_preparation.Record_splines import record_splines
from PhyTrade.Tools.DATA_SLICE_gen import data_slice


def gen_ticker_metalabels(settings, ticker):
    ref_data_slice = data_slice(ticker,
                                settings.market_settings.testing_start_date,
                                settings.market_settings.data_slice_size, 0,
                                end_date=settings.market_settings.testing_end_date)

    settings.market_settings.testing_end_date = ref_data_slice.stop_date

    while not ref_data_slice.end_of_dataset:
        # --> Run optimiser on current slice
        evo_optimisation = EVOA_optimiser(settings, ticker, optimiser_setting=2)
        record_splines(evo_optimisation.best_individual.parameter_dictionary, evo_optimisation.data_slice, ticker)

        # --> Get next data slice and update settings
        ref_data_slice.get_shifted_data_slice()
        settings.market_settings.testing_start_date = ref_data_slice.start_date
        settings.market_settings.testing_end_date = ref_data_slice.stop_date
