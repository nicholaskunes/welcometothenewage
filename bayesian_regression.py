# -*- coding: utf-8 -*-

import numpy as np
import bigfloat as bg
from numpy.linalg import norm
from sklearn import linear_model
from sklearn.cluster import KMeans


def generate_timeseries(prices, n):
    m = len(prices) - n
    ts = np.empty((m, n + 1))
    for i in range(m):
        ts[i, :n] = prices[i:i + n]
        ts[i, n] = prices[i + n] - prices[i + n - 1]
    return ts


def find_cluster_centers(timeseries, k):
    k_means = KMeans(n_clusters=k)
    k_means.fit(timeseries)
    return k_means.cluster_centers_


def choose_effective_centers(centers, n):
    return centers[np.argsort(np.ptp(centers, axis=1))[-n:]]


def predict_dpi(x, s):
    num = 0
    den = 0
    for i in range(len(s)):
        y_i = s[i, len(x)]
        x_i = s[i, :len(x)]
        exp = bg.exp(-0.25 * norm(x - x_i) ** 2)
        num += y_i * exp
        den += exp
    return num / den



def linear_regression_vars(prices, v_bid, v_ask, s1, s2, s3):
    X = np.empty((len(prices) - 721, 4))
    Y = np.empty(len(prices) - 721)
    for i in range(720, len(prices) - 1):
        dp = prices[i + 1] - prices[i]
        dp1 = predict_dpi(prices[i - 180:i], s1)
        dp2 = predict_dpi(prices[i - 360:i], s2)
        dp3 = predict_dpi(prices[i - 720:i], s3)
        r = (v_bid[i] - v_ask[i]) / (v_bid[i] + v_ask[i])
        X[i - 720, :] = [dp1, dp2, dp3, r]
        Y[i - 720] = dp
    return X, Y


def find_parameters_w(X, Y):
    clf = linear_model.LinearRegression()
    clf.fit(X, Y)
    w0 = clf.intercept_
    w1, w2, w3, w4 = clf.coef_
    return w0, w1, w2, w3, w4


def predict_dps(prices, v_bid, v_ask, s1, s2, s3, w):
    dps = []
    w0, w1, w2, w3, w4 = w
    for i in range(720, len(prices) - 1):
        dp1 = predict_dpi(prices[i - 180:i], s1)
        dp2 = predict_dpi(prices[i - 360:i], s2)
        dp3 = predict_dpi(prices[i - 720:i], s3)
        r = (v_bid[i] - v_ask[i]) / (v_bid[i] + v_ask[i])
        dp = w0 + w1 * dp1 + w2 * dp2 + w3 * dp3 + w4 * r
        dps.append(float(dp))
    return dps


def evaluate_performanceSNYTH(prices, dps, t, step):
    """Use the third time period to evaluate the performance of the algorithm.
    Args:
        prices: A numpy array of floats representing prices over the third time
            period.
        dps: A numpy array of floats generated by predict_dps().
        t: A number representing a threshold.
        step: An integer representing time steps (when we make trading decisions).
    Returns:
        A number representing the bank balance.
    """
    bank_balance = 0
    position = 0
    for i in range(720, len(prices) - 1, step):
        # long position - BUY
        if dps[i - 720] > t and position <= 0:
            position += 1
            bank_balance -= prices[i]
        # short position - SELL
        if dps[i - 720] < -t and position >= 0:
            position -= 1
            bank_balance += prices[i]
    # sell what you bought
    if position == 1:
        bank_balance += prices[len(prices) - 1]
    # pay back what you borrowed
    if position == -1:
        bank_balance -= prices[len(prices) - 1]
    return bank_balance

def evaluate_performance(prices, v_bid, v_ask, s1, s2, s3, w, t, step):
    dps = []
    w0, w1, w2, w3, w4 = w
    for i in range(720, len(prices) - 1):
        dp1 = predict_dpi(prices[i - 180:i], s1)
        dp2 = predict_dpi(prices[i - 360:i], s2)
        dp3 = predict_dpi(prices[i - 720:i], s3)
        r = (v_bid[i] - v_ask[i]) / (v_bid[i] + v_ask[i])
        dp = w0 + w1 * dp1 + w2 * dp2 + w3 * dp3 + w4 * r
        dps.append(float(dp))
        
    bank_balance = 0
    position = 0
    for i in range(720, len(prices) - 1, step):
        # long position - BUY
        if dps[i - 720] > t and position <= 0:
            position += 1
            bank_balance -= prices[i]
        # short position - SELL
        if dps[i - 720] < -t and position >= 0:
            position -= 1
            bank_balance += prices[i]
    # sell what you bought
    if position == 1:
        bank_balance += prices[len(prices) - 1]
    # pay back what you borrowed
    if position == -1:
        bank_balance -= prices[len(prices) - 1]
    return bank_balance
