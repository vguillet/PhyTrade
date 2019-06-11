import numpy as np


class MATH_tools:
    @staticmethod
    def normalise_zero_one(signal):

        signal_normalised = np.zeros(len(signal))
        
        for i in range(len(signal)):
            signal_normalised[i] = (signal[i]-min(signal))/((max(signal)-min(signal)) or 1)
        
        return signal_normalised
    
    @staticmethod
    def normalise_minus_one_one(signal):
        signal_normalised = np.zeros(len(signal))

        for i in range(len(signal)):
            signal_normalised[i] = 2*(signal[i] - min(signal)) / ((max(signal) - min(signal)) or 1)-1

        return signal_normalised

    @staticmethod
    def amplify(signal, amplification_factor):

        signal_amplified = np.zeros(len(signal))

        for i in range(len(signal)):
            signal_amplified[i] = signal[i]*amplification_factor

        return signal_amplified

    @staticmethod
    def best_fit(X, Y):
        xbar = sum(X) / len(X)
        ybar = sum(Y) / len(Y)
        n = len(X)  # or len(Y)

        numer = sum([xi * yi for xi, yi in zip(X, Y)]) - n * xbar * ybar
        denum = sum([xi ** 2 for xi in X]) - n * xbar ** 2

        b = numer / denum
        a = ybar - b * xbar

        # print('best fit line:\ny = {:.2f} + {:.2f}x'.format(a, b))

        return a, b
