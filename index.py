# print("hello");

# while(True):
#     print('hello');

# for x in [1,4,5,6]:
#     print(x)

# for x in range(10):
#     print(x)

# if(condition1):
#     do this
# elif(condition2):
#     do that
# else:
#     then do this

import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr

yf.pdr_override()

stock=input("enter stock ticker symbol: ")
print(stock)

startyear=2019
startmonth=1
startday=1

start=dt.datetime(startyear,startmonth,startday)

now=dt.datetime.now()

df=pdr.get_data_yahoo(stock,start,now)

print(df)

ma=50

smaString="Sma_"+str(ma)

df[smaString]=df.iloc[:,4].rolling(window=ma).mean()

# print(df)

df=df.iloc[ma:]

# print(df)

for i in df.index:
    if(df["Adj Close"][i]>df[smaString][i]):
        print("The close is higher")
    else:
        print("The close is lower")
    # print(df[smaString][i])
    # print(df["Adj Close"][i])
    # print(df.iloc[:,4][i])