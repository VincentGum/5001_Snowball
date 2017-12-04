#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 17:26:34 2017

compute the rsi of every industry and save as a csv

@author: llr
"""

#preprocessing

import numpy as np
import pandas as pd
import unicodecsv
import talib

#generate history


def get_states():
    enrollments = []
    with open('Snowball/Evaluation_Demo/industry_quote.csv', 'rb') as f:
        quote = unicodecsv.reader(f)
        for row in quote:
            enrollments.append(row)

    enrollments2 = np.zeros((len(enrollments) - 1, 29))

    for i in range(1, len(enrollments)):
        for j in range(1, 30):
            enrollments2[i - 1][j - 1] = float(enrollments[i][j])

    feature0, feature1, feature2 = 0, 0, 0

    average10 = np.zeros((len(enrollments) - 1, 29))

    for i in range(0, 29):
        for j in range(9, len(enrollments2)):
            average10[j][i] = np.mean(enrollments2[j - 9:j, i])

    average10_all = np.zeros((len(enrollments) - 1, 1))

    average10_all = np.sum(average10, axis=1)

    average10_all_copy = np.array(average10_all)

    average10_all_copy.sort()

    inte0 = average10_all_copy[120]
    inte1 = average10_all_copy[230]
    inte2 = average10_all_copy[340]
    inte3 = average10_all_copy[450]
    inte4 = average10_all_copy[560]

    level_mean10 = np.zeros((len(average10_all),))

    for i in range(len(average10_all)):
        item_current = average10_all[i]
        if item_current < inte0:
            level_mean10[i] = 0
        elif item_current < inte1:
            level_mean10[i] = 0.2
        elif item_current < inte2:
            level_mean10[i] = 0.4
        elif item_current < inte3:
            level_mean10[i] = 0.6
        elif item_current < inte4:
            level_mean10[i] = 0.8
        else:
            level_mean10[i] = 1

    level_updown = np.zeros((len(average10_all),))

    for i in range(10, len(average10_all)):
        if average10_all[i] <= average10_all[i - 1]:
            level_updown[i] = 0
        else:
            level_updown[i] = 1

    rsi_period = 10
    rsi_total = talib.RSI(average10_all, timeperiod=rsi_period)
    level_rsi = np.zeros((len(average10_all),))
    for i in range(10, len(average10_all)):
        level_rsi[i] = round(rsi_total[i] / 100, 1)

    states = np.column_stack((level_mean10, level_updown, level_rsi))
    df = pd.DataFrame(states, columns={'mean10', 'updown', 'rsi'})
    return df

