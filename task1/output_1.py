import pandas as pd
import numpy as np
date = pd.read_csv('Snowball/quote.csv')


date = list(date['TradingDay'])
date = date[10:658]

strategy = open('task1_strategy', 'r')
strs = []

for i in strategy.readlines():
    strs.append(i[0:6])

weight = []
for i in range(648):
    weight.append(0.8)

dates = []
for i in date:
    dates.append(i)

df = pd.DataFrame()

df.insert(0, 'stockweight', weight)
df.insert(0, 'stockcode', strs)
df.insert(0, 'tradingday', dates)
df.to_csv('op_1.csv', index=False)

