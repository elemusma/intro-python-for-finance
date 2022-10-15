import yfinance as yf
import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import statistics
import numpy as np
import matplotlib.ticker as mticker

yf.pdr_override() #activate yahoo finance workaround
year=1980 #set start year
start=dt.datetime(year,1,1) #sets start point of dataframe
now=dt.datetime.now() #sets end point of dataframe

stock=input("Enter the stock symbol : ") #asks for stock ticker

while stock != "quit": #runs this loop until user enters 'quit' (can do many stocks in a row)

    fig,ax1=plt.subplots()
    df=pdr.get_data_yahoo(stock, start, now)

    sma=int(input("Enter a sma: "))
    limit=int(input("Enter warning limit: "))

    #calculates moving average
    df['SMA'+str(sma)] = df.iloc[:,4].rolling(window=sma).mean() #the df.iloc is the adj close col
    #calculates percent change
    df['PC'] = ((df['Adj Close']/df['SMA'+str(sma)])-1)*100

    mean=df['PC'].mean()
    stdev=df['PC'].std()

    current=df['PC'][-1]
    yday=df['PC'][-1]

    print("Mean: "+str(mean))
    print("STDEV: "+str(stdev))

    bins=np.arange(-100,100,1)

    plt.xlim([df["PC"].min()-5,df["PC"].max()+5])

    plt.hist(df["PC"],bins=bins,alpha=.5)
    plt.title(stock+"-- % From "+str(sma)+" SMA Histogram since "+str(year)) #set title
    plt.xlabel('Percent from '+str(sma)+' SMA (bin size = 1)') #set x axis title
    plt.ylabel('Count') #set y axis title

    plt.axvline(x=mean,ymin=0,ymax=1,color='k',linestyle='--')
    plt.axvline(x=mean+stdev,ymin=0,ymax=1,color='gray',linestyle='--')
    plt.axvline(x=mean+2*stdev,ymin=0,ymax=1,color='gray',linestyle='--')
    plt.axvline(x=mean+3*stdev,ymin=0,ymax=1,color='gray',linestyle='--')

    plt.axvline(x=mean-stdev,ymin=0,ymax=1,color='gray',linestyle='--')
    plt.axvline(x=mean-2*stdev,ymin=0,ymax=1,color='gray',linestyle='--')
    plt.axvline(x=mean-3*stdev,ymin=0,ymax=1,color='gray',linestyle='--')

    plt.axvline(x=current,ymin=0,ymax=1,color='r')
    plt.axvline(x=yday,ymin=0,ymax=1,color='gray')

    ax1.xaxis.set_major_locator(mticker.MaxNLocator(14))

    fig2, ax2=plt.subplots()

    df=df[-150:]

    df["PC"].plot(label="close", color="k")
    plt.title(stock+"-- % From "+str(sma)+" Over the past 150 days "+str(year)) #set title
    plt.xlabel('Date') #set x axis title
    plt.ylabel('Percent from '+str(sma)) #set y axis title

    ax2.xaxis.set_major_locator(mticker.MaxNLocator(8))

    plt.axhline(y=current,xmin=0,xmax=1,color='r')
    plt.show()

    stock=input("Enter the stock symbol : ") #asks for stock ticker