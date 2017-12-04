import pandas as pd
import numpy as np
date = pd.read_csv('Snowball/Evaluation_Demo/industry_quote.csv')
date = list(date['tradingday'])
date = date[10:658]

strategy = open('task3_strategy', 'r')
strs = []

for i in strategy.readlines():
    ins = i.split(',')
    strs.append(ins[0])
    strs.append(ins[1])
    strs.append(ins[2][0:11])

weight = []
for i in range(648):
    weight.append(0.3)
    weight.append(0.3)
    weight.append(0.3)

dates = []
for i in date:
    dates.append(i)
    dates.append(i)
    dates.append(i)

df = pd.DataFrame()

df.insert(0, 'industryweight', weight)
df.insert(0, 'industrycode', strs)
df.insert(0, 'tradingday', dates)
df.to_csv('op_3.csv')