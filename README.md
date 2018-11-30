Author: Victor Guillet
11/28/2018
_______________________________________________________________________________________________
"Econophysics is an interdisciplinary research field, applying theories and methods originally developed by physicists
in order to solve problems in economics, usually those including uncertainty or stochastic processes
and nonlinear dynamics. Some of its application to the study of financial markets has also been termed
statistical finance referring to its roots in statistical physics."

https://en.wikipedia.org/wiki/Econophysics
_______________________________________________________________________________________________

This library is currently being buit up, come back to this file to stay up to date with the latest developments

The Phytrade library is developed for trading using a combination of classic economics methods along with a number
of physics principles. The library is structured as follow:

- A big_data object instance must be initialised, and the dataset must be provided (for now the library is tailored
to work with Quandl). 

-Once created, a number of indicator scripts can be used to compute different properties of the dataset. 

Ex: For determining the rsi of the dataset using a specific set of settings, an rsi class instance 
should be generated (using the wanted parameters) and stored in big_data as one of it's attributes. 
Doing this allows for an easy circulation of information and enables multiple
instances of the same indicator to be computed with different parameters.

-The big_data instance is then to be passed on to every function and class which require access to the dataset's 
determined properties
To access a specific attributes, use: big_data."name of starred instance which's property you want to access".property
_______________________________________________________________________________________________



A list of possible attributes/functions to be computed by the library and the classes required: 


--------------- Big_data storage class:

BIGDATA(data, ticker, data_slice_start_ind, data_slice_stop_ind)

    P   ticker              : Ticker of the dataset
    P   data                : Data collected
        dates               : Dates of the data
        data_close_values   : List of close values in data slice
        data_open_values    : List of open values in data slice

    P   data_slice_start_ind		    : Starting index of data slice
    P   data_slice_stop_ind         	: Stopping index of data slice
        data_slice                  	: Data slice (data falling in range of the start/stop indices)
        data_slice_dates            	: Dates of the data slice
        data_slice_close_values     	: List of close values in data slice
        data_slice_open_values      	: List of open values in data slice

        values_fluctuation          	: Fluctuation of values in data slice
        close_values_gradient       	: Gradient of close values in data slice
        open_values_gradient        	: Gradient of open values in data slice

        oc_avg_gradient_bb_signal   	: OC gradient bull-bear signal

        sell_trigger_values         	: Sell values matching sell triggers (initially empty list, to fill using calc_trigger_values from OC module)
        buy_trigger_values          	: Buy values matching sell triggers (initially empty list, to fill using calc_trigger_values from OC module)

========================== Indicators (to be set as big_data attributes) ======================

--------------- RSI indicator:

RSI(big_data, timeframe=14, buffer_setting=0)

    P   timeframe           	: Time frame to be used by RSI module (default = 14)
    P   buffer_setting      	: Buffer setting to be used by RSI module (default = 0)

        rsi_values          	: RSI values for data slice
        upper_bound         	: Dynamic upper bound for data slice
        lower_bound         	: Dynamic lower bound for data slice

        sell_dates          	: RSI trigger sell dates
        buy_dates           	: RSI trigger buy dates

        sell_rsi            	: RSI sell rsi
        buy_rsi             	: RSI buy rsi

        bb_signal           	: RSI bull-bear signal

    --> plot_rsi_and_bounds(big_data, plot_rsi=True, plot_upper_bound=True, plot_lower_bound=True, plot_trigger_signals=True):

--------------- SMA indicator:

SMA(big_data, timeperiod_1=50, timeperiod_2=200)

    P   timeperiod_1         	: First time period to be used by SMA module (default = 50)
    P   timeperiod_2         	: Second time period to be used by SMA module (default = 200)
	sma_1		     			: SMA calculated for the first time period
	sma_2		     			: SMA calculated for the second time period
	bb_signal		    		: SMA bull-bear signal

    --> plot_sma(self, big_data, plot_sma_1=True, plot_sma_2=True, plot_trigger_signals=True):

        
================================= Tools =========================================

--------------- OC module:
    --> calc_trigger_values(big_data, sell_dates, buy_dates):
            sell_trigger_values
            buy_trigger_values

    --> plot_open_close_values(big_data, plot_close_values=True, plot_open_values=True):

    --> plot_open_close_values_diff(big_data):

    --> plot_trigger_values(big_data):

--------------- SPLINE module:

        spline_x            	: x value array for spline calculation
        spline_xs           	: xs value array for spline calculation

    --> calc_signal_spline(big_data, signal, smoothing_factor=0.7):
            spline_length      	: length of splines
	    >return spline         	: generated spline from input signal

    --> combine_signal_splines(big_data, signals):
            >return combined_signal_splines : combined selected signal spline

    --> combine_weighted_signal_splines(big_data, signal_1, signal_2, signal_3, weight_1=1, weight_2=1, weight_3=1)
            >return combined_signal_splines : combined selected signal spline with matching weights
    
    --> plot_signal_spline(big_data, spline, label, color='g'):

    --> calc_upper_lower_threshold(big_data):




Notes:
Signal combination:
The weight associated with each signal in the signal addition should be selected according to the
type and period of trade. For trading on the short term, short term indicators should be weighted higher
while on the long term, longer term indicators should be dominant














