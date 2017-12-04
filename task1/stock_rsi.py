#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec  3 20:54:22 2017

@author: llr
"""

import numpy as np
import unicodecsv
import pandas as pd
import operator
import talib

def get_rsi():
    enrollments_record = []
    with open('Snowball/quote.csv','rb') as f2:
        quote = unicodecsv.reader(f2)
        for row in quote:
            enrollments_record.append(row)



    rsi_period=10
    #times_stock=[]
    times_temp=1
    stocks=[]
    close_price=[]
    j=0
    close_price.append(enrollments_record[1][0])
    close_price.append(enrollments_record[1][3])

    for i in range(2,len(enrollments_record)):
        if  enrollments_record[i][0]== enrollments_record[i-1][0]:
            times_temp+=1
            close_price.append(enrollments_record[i][3])
        else:
            if times_temp==719:
                close_copy=close_price[:]
                stocks.append(close_copy)
            #times_stock.append(times_temp)
            times_temp=1
            close_price.clear()
            close_price.append(enrollments_record[i][0])
            close_price.append(enrollments_record[i][3])

    rsi_stock=[]
    rsi_stocks=[]
    for i in range(len(stocks)):
        temp=np.array(stocks[i])
        temp1=temp[1:]
        close=[]
        for item in temp1:
            close.append(float(item))
        close_array=np.array(close)
        rsi_stock=talib.RSI(close_array, timeperiod = rsi_period)
        rsi_stocks.append(rsi_stock)

    rsi_stocks=np.array(rsi_stocks)
    rsi_stocks2=rsi_stocks[:,:668]

    temp=np.array(stocks)
    id_stocks=temp[:,0]

    df = pd.DataFrame(rsi_stocks2, index=id_stocks)

    return df