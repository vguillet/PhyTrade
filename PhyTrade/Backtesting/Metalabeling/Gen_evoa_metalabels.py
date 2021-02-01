
##################################################################################################################
"""
Used to generate metalabels using the EVO algorithm
"""

# Built-in/Generic Imports
from math import ceil

# Own modules
from PhyTrade.Signal_optimisation.EVO_algorithm.EVO_algorithm import EVO_algorithm
from PhyTrade.Data_Collection_preparation.Record_splines import record_splines
from PhyTrade.Building_blocks.Trading_dataslice import Trading_dataslice
from PhyTrade.Tools.Progress_bar_tool import Progress_bar


__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

##################################################################################################################


def gen_ticker_metalabels(settings, ticker):
    settings.signal_tuning_settings.gen_evoa_metalabels_settings()
    settings.fetch_dates(settings.signal_tuning_settings.optimiser_setting)

    if settings.signal_tuning_settings.multiprocessing is False:
        print("\n==================================================================================")
        print("=====================", ticker, "Metalabels generation initiated =======================")
        print("==================================================================================\n")

    # --> Generate reference data slice
    ref_data_slice = Trading_dataslice(ticker=ticker,
                                       start_date=settings.start_date,
                                       subslice_size=settings.market_settings.subslice_size,
                                       subslice_shift_per_step=0,
                                       end_date=settings.end_date)

    nb_slices = ceil((-ref_data_slice.start_index+ref_data_slice.end_index) / ref_data_slice.default_subslice_size)

    # --> Print initial progress and status
    if settings.signal_tuning_settings.multiprocessing is False:
        print("Total date interval processed:", ref_data_slice.start_date, ref_data_slice.end_date)

    progress_bar = Progress_bar(max_step=nb_slices, bar_size=60, label=ticker + " metalabeling", overwrite_setting=False)

    while not ref_data_slice.end_of_dataset:
        if settings.signal_tuning_settings.multiprocessing is False:
            print("\n------------------------------------------------------------------> Date slice processed:",
                  str(ref_data_slice.subslice_start_date) + " --> " + str(ref_data_slice.subslice_stop_date))

        # --> Run optimiser on ref data slice
        evo_optimisation = EVO_algorithm(settings=settings,
                                         ticker=ticker,
                                         optimiser_setting=settings.signal_tuning_settings.optimiser_setting,
                                         data_slice=ref_data_slice)

        # --> Record results
        record_splines(parameter_set=evo_optimisation.best_individual.parameter_set,
                       data_slice=evo_optimisation.data_slice,
                       ticker=ticker)

        # --> Get next data slice
        ref_data_slice.get_next_subslice()

        # --> Print Progress and status
        progress_bar.update_progress()

    if settings.signal_tuning_settings.multiprocessing is False:
        print("\n=====================", ticker, "Metalabels generated successfully =====================\n")
