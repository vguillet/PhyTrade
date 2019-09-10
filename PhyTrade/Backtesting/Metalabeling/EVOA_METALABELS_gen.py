
##################################################################################################################
"""
Used to generate metalabels using the EVOA optimiser algorithm
"""

# Built-in/Generic Imports
from math import ceil

# Own modules
from PhyTrade.Signal_optimisation.EVOA_optimisation.EVO_algo_4 import EVOA_optimiser
from PhyTrade.Data_Collection_preparation.Record_splines import record_splines
from PhyTrade.Tools.DATA_SLICE_gen import data_slice
from PhyTrade.Tools.Progress_bar_tool import Progress_bar


__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

##################################################################################################################

def gen_ticker_metalabels(settings, ticker):
    settings.signal_training_settings.gen_evoa_metalabels_settings()
    settings.fetch_dates(settings.signal_training_settings.optimiser_setting)

    if settings.signal_training_settings.multiprocessing is False:
        print("\n==================================================================================")
        print("=====================", ticker, "Metalabels generation initiated =======================")
        print("==================================================================================\n")
    ref_data_slice = data_slice(ticker,
                                settings.start_date,
                                settings.market_settings.data_slice_size, 0,
                                end_date=settings.end_date)

    nb_slices = ceil((-ref_data_slice.default_start_index+ref_data_slice.default_end_index)/ref_data_slice.default_slice_size)

    # --> Print initial progress and status
    if settings.signal_training_settings.multiprocessing is False:
        print(ref_data_slice.default_start_date, ref_data_slice.default_end_date)

    progress_bar = Progress_bar(max_step=nb_slices, bar_size=60, label=ticker+" metalabeling", overwrite_setting=False)

    # --> Overwrite training dates with testing dates in settings
    settings.market_settings.training_start_date = ref_data_slice.start_date
    settings.market_settings.training_end_date = ref_data_slice.stop_date

    while not ref_data_slice.end_of_dataset:
        if settings.signal_training_settings.multiprocessing is False:
            print("\nDate slice processed:", ref_data_slice.start_date + " --> " + ref_data_slice.stop_date)

        # --> Run optimiser on current slice
        evo_optimisation = EVOA_optimiser(settings, ticker, optimiser_setting=settings.signal_training_settings.optimiser_setting)
        record_splines(evo_optimisation.best_individual.parameter_dictionary, evo_optimisation.data_slice, ticker)

        # --> Get next data slice and update settings
        ref_data_slice.get_next_data_slice()
        settings.start_date = ref_data_slice.start_date
        settings.end_date = ref_data_slice.stop_date

        # --> Print Progress and status
        progress_bar.update_progress()

    if settings.signal_training_settings.multiprocessing is False:
        print("\n=====================", ticker, "Metalabels generated successfully =====================\n")
