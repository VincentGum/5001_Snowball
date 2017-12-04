# -*- coding: utf-8 -*-
"""
Created on Fri Nov 17 17:26:34 2017

compute the rsi of every industry and save as a csv

@author: VincentGum
"""

import pandas as pd
from task1 import q_1
from task1 import states_1

from task1 import stock_rsi

industry_quote = pd.read_csv('Snowball/Evaluation_Demo/industry_quote.csv')
industry_code = list(industry_quote.columns)[1:]

stock_rsi = stock_rsi.get_rsi()

print(stock_rsi[111]['000429'])




# Get Actions
ACTIONS = []
for i in stock_rsi.index:
    ACTIONS.append(i)

REWARD_RULE = stock_rsi
STATES = states_1.get_states()

q = q_1.q_unit(STATES, ACTIONS, REWARD_RULE)
q_table, strategy = q.learn()

q_table.to_csv('task1_q.csv')
file = open('task1_strategy', 'w')
for i in strategy:
    file.write(i)
    file.write('\n')

