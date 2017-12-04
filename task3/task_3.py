# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 17:26:34 2017

compute the rsi of every industry and save as a csv

@author: VincentGum
"""

import numpy as np
import pandas as pd
import talib
import unicodecsv

from task3 import states_3
from task3 import q_3

industry_quote = pd.read_csv('../Snowball/Evaluation_Demo/industry_quote.csv')
industry_code = list(industry_quote.columns)[1:]


# Get Actions
ACTIONS = []

for i in range(0, len(industry_code) - 2):
    for j in range(i + 1, len(industry_code) - 1):
        for k in range(j + 1, len(industry_code)):
            string = industry_code[i] + ',' + industry_code[j] + ',' + industry_code[k]
            ACTIONS.append(string)


# generate rsi
enrollments = []
with open('../Snowball/Evaluation_Demo/industry_quote.csv', 'rb') as f:
    quote = unicodecsv.reader(f)
    for row in quote:
        enrollments.append(row)

enrollments[0]
rsi_period = 10
enrollments2 = np.zeros((len(enrollments) - 1, 29))

for i in range(1, len(enrollments)):
    for j in range(1, 30):
        enrollments2[i - 1][j - 1] = float(enrollments[i][j])

rsi = []
for i in range(29):
    rsi.append(talib.RSI(enrollments2[:, i], timeperiod=rsi_period))

temp = np.array(rsi).T
industry_rsi_df = pd.DataFrame(temp)
industry_rsi_df.columns = industry_code


REWARD_RULE = industry_rsi_df
STATES = states_3.get_states()


q = q_3.q_unit(STATES, ACTIONS, REWARD_RULE)
q_table, strategy = q.learn()
q_table.to_csv('task3_q.csv')
file = open('task3_strategy', 'w')
for i in strategy:
    file.write(i)
    file.write('\n')



