import numpy as np
from numpy import genfromtxt

np.set_printoptions(threshold=3)
np.set_printoptions(suppress=True)


# Notation used coming from: https://www.bzarg.com/p/how-a-kalman-filter-works-in-pictures/


def prediction(X_hat_t_1, P_t_1, F_t, B_t, U_t, Q_t):
    """
    The new best estimate is a prediction made from previous best estimate,
    plus a correction for known external influences. And the new uncertainty is predicted
    from the old uncertainty, with some additional uncertainty from the environment.

    :param X_hat_t_1: previous best estimate
    :param P_t_1: old uncertainty
    :param F_t: prediction
    :param B_t: correction
    :param U_t: known external influences
    :param Q_t: additional uncertainty from the environment
    :return: X_hat_t, P_t: new best estimate, new uncertainty
    """

    X_hat_t = F_t.dot(X_hat_t_1) + (B_t.dot(U_t).reshape(B_t.shape[0], -1))
    P_t = np.diag(np.diag(F_t.dot(P_t_1).dot(F_t.transpose()))) + Q_t
    return X_hat_t, P_t


def update(X_hat_t, P_t, Z_t, R_t, H_t):
    """
    :param X_hat_t: Current best estimate
    :param P_t: Current uncertainty
    :param Z_t: Observed mean
    :param R_t: Observed covariance (sensor noise)
    :param H_t: Sensor matrix
    :return: X_t, P_t: new best estimate, new uncertainty
    """
    K_prime = P_t.dot(H_t.transpose()).dot(np.linalg.inv(H_t.dot(P_t).dot(H_t.transpose()) + R_t))
    print("K:\n", K_prime)

    X_t = X_hat_t + K_prime.dot(Z_t - H_t.dot(X_hat_t))
    P_t = P_t - K_prime.dot(H_t).dot(P_t)

    return X_t, P_t


acceleration = 0
delta_t = 1 / 20  # milisecond

groundTruth = genfromtxt('data/groundTruth.csv', delimiter=',', skip_header=1)

# Observations: position_X, position_Y
measurmens = genfromtxt('data/measurmens.csv', delimiter=',', skip_header=1)

# Checking our result with OpenCV
opencvKalmanOutput = genfromtxt('data/kalmanv.csv', delimiter=',', skip_header=1)

# Transition matrix
F_t = np.array([[1, 0, delta_t, 0], [0, 1, 0, delta_t], [0, 0, 1, 0], [0, 0, 0, 1]])

# Initial State cov
P_t = np.identity(4) * 0.2

# Process cov
Q_t = np.identity(4)

# Control matrix
B_t = np.array([[0], [0], [0], [0]])

# Control vector
U_t = acceleration

# Measurment Matrix
H_t = np.array([[1, 0, 0, 0], [0, 1, 0, 0]])

# Measurment cov
R_t = np.identity(2) * 5

# Initial State
X_hat_t = np.ar_t, X_haray([[0], [0], [0], [0]])
print("X_hatt_t.shape")
print("P_t", P_t.shape)
print("F_t", F_t.shape)
print("B_t", B_t.shape)
print("Q_t", Q_t.shape)
print("R_t", R_t.shape)
print("H_t", H_t.shape)

for i in range(measurmens.shape[0]):
    X_hat_t, P_hat_t = prediction(X_hat_t, P_t, F_t, B_t, U_t, Q_t)
    print("Prediction:")
    print("X_hat_t:\n", X_hat_t, "\nP_t:\n", P_t)

    Z_t = measurmens[i].transpose()
    Z_t = Z_t.reshape(Z_t.shape[0], -1)

    print(Z_t.shape)

    X_t, P_t = update(X_hat_t, P_hat_t, Z_t, R_t, H_t)
    print("Update:")
    print("X_t:\n", X_t, "\nP_t:\n", P_t)
    X_hat_t = X_t
    P_hat_t = P_t

    print("=========================================")
    print("Opencv Kalman Output:")
    print("X_t:\n", opencvKalmanOutput[i])