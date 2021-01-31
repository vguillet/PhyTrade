
##################################################################################################################
"""
This class is used to generate Kalman filters.
It is based on the Kalman filter code found at:
 https://towardsdatascience.com/kalman-filters-a-step-by-step-implementation-guide-in-python-91e7e123b968
"""

# Built-in/Generic Imports
from math import *

# Libs
import matplotlib.pyplot as plt
import numpy as np

# Own modules

__version__ = '1.1.1'
__author__ = 'Victor Guillet'
__date__ = '10/09/2019'

##################################################################################################################


# gaussian function
def gen_gaussian(mean, squared_variance, x):
    """
    Use to obtain Gaussian value from a gaussian distribution
    :param mean: Mean of distribution
    :param squared_variance: Squared variance of distribution
    :param x: Input x
    :return: Gaussian value
    """

    coefficient = 1.0 / sqrt(2.0 * pi * squared_variance)
    exponential = exp(-0.5 * (x-mean) ** 2 / squared_variance)
    return coefficient * exponential


# the update function
def update(means, variances):
    """
    This function takes in a list of mean and variance terms,
    and returns updated gaussian parameters

    The length of the mean and variance lists must be equal

    :param means: List of means
    :param variances: List of variances
    :return: Updated gaussian parameters list(new_mean, new_variance)
    """
    assert(len(means) == len(variances))
    # Calculate the new parameters
    summation = 0
    sum_var = 0
    for i in range(len(means)):
        summation += means[i] + variances[i]
        sum_var += 1/variances[i]

    new_mean = summation / sum(variances)
    new_variance = 1 / sum_var

    return [new_mean, new_variance]


# the motion update/predict function
def predict(means, variances):
    """
    This function takes in two means and two squared variance terms,
    and returns updated gaussian parameters, after motion

    :param means: List of means
    :param variances: List of variances
    :return: Updated gaussian parameters
    """

    # Calculate the new parameters
    new_mean = sum(means)
    new_var = sum(variances)

    return [new_mean, new_var]


# measurements for mu and motions, U
measurements = [5., 6., 7., 9., 10.]
motions = [1., 1., 2., 1., 1.]

# initial parameters
measurement_sig = 4.
motion_sig = 2.
mu = 0.
sig = 10000.

## TODO: Loop through all measurements/motions
# this code assumes measurements and motions have the same length
# so their updates can be performed in pairs
for n in range(len(measurements)):
    # measurement update, with uncertainty
    mu, sig = update(mu, sig, measurements[n], measurement_sig)
    print('Update: [{}, {}]'.format(mu, sig))
    # motion update, with uncertainty
    mu, sig = predict(mu, sig, motions[n], motion_sig)
    print('Predict: [{}, {}]'.format(mu, sig))

# print the final, resultant mu, sig
print('\n')
print('Final result: [{}, {}]'.format(mu, sig))

## Print out and display the final, resulting Gaussian
# set the parameters equal to the output of the Kalman filter result
mu = mu
sigma2 = sig

# define a range of x values
x_axis = np.arange(-20, 20, 0.1)

# create a corresponding list of gaussian values
g = []
for x in x_axis:
    g.append(f(mu, sigma2, x))

# plot the result
plt.plot(x_axis, g)