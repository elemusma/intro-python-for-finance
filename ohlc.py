import yfinance as yf
import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import datetime as datetime
import numpy as np
from mpl_finance import candlestick_ohlc

yf.pdr_override() #activate yahoo finance workaround

smasUsed=[10,30,50] #choose smas, 10 day simple, 30 day simple, 50 day simple

start=dt.datetime(2020,1,1)-dt.datetime(days=max(smasUsed)) #sets start point of dataframe
now=dt.datetime.now() #sets end point of dataframe
stock=input("Enter the stock symbol : ") #asks for stock ticker

while stock != "quit": #runs this loop until user enters 'quit' (can do many stocks in a row)
    prices=pdr.get_data_yahoo(stock,start,now) #fetches stock price data, saves as data frame

    fig,ax1=plt.subplots() #create plots
    #calculate moving averages
    for x in smasUsed: #this for loop calculates the SMAs for the stated periods and appends to dataframe
        sma=x
        prices['SMA_'+str(sma)]=prices.iloc[:,4].rolling(window=sma).mean() #calculates sma and creates col
    
    #calculate bollinger bands
    BBperiod=15 #choose moving average - 20 is the standard
    stdev=2 #std means standard deviation
    prices['SMA'+str(BBperiod)]=prices.iloc[:,4].rolling(window=BBperiod).mean() #calculates sma and creates a column
    prices['STDEV']=prices.iloc[:,4].rolling(window=BBperiod).std() #calculates standard deviation and creates col
    prices['LowerBand']=prices['SMA'+str(BBperiod)]-(stdev*prices['STDEV']) #calculates lower bollinger band
    prices['UpperBand']=prices['SMA'+str(BBperiod)]+(stdev*prices['STDEV']) #calculates upper band
    prices['Date']=mdates.date2num(prices.index) #creates a date column stored in number format (for OHLC bars), this is a converted date column from a timestamp to a number

    #calculate 10.4.4 stochastic
    Period=10 #choose stoch period
    K=4 #choose K parameter
    D=4 #choose D parameter

    prices["RolHigh"]=prices["High"].rolling(window=Period).max() #finds high of period
    prices["RolLow"]=prices["Low"].rolling(window=Period).min() #finds low of period
    prices["stok"]=((prices["Adj Close"]-prices["Rollow"])/(prices["RolHigh"]-prices["RolLow"]))*100 #Finds 10.1 stoch
    prices["K"]=prices["stok"].rolling(window=K).mean() #finds 10.4 stoch
    prices["D"]=prices["K"].rolling(window=D).mean() #finds 10.4.4 stoch
    prices["GD"]=prices["High"] #creates GD column to store green dots

    ohlc=[] #create OHLC array which will store price data for the candlestick chart

    #delete extra dates
    prices=prices.iloc[max(smasUsed):]

    greenDotDate=[] #Stores dates of Green Dots
    greenDot=[] #Stores values of green dots
    lastK=0 #will store yesterday's fast stoch
    lastD=0 #will store yesterday's slow stoch
    lastLow=0 #will store yesterdays lower
    lastClose=0 #will store yesterdays close
    lastLowBB=0 #will store yesterdays lower band

    #go through price history to create candlesticks and GD+Blue dots
    for i in prices.index:
        #append OHLC prices to make the candlestick
        append_me=prices["Date"][i],prices["Open"],prices["High"],prices["Low"],prices["Adj Close"],prices["Volume"][i]
        ohlc.append(append_me)

        #check for green dot
        if prices['K'][i]>prices['D'][i] and lastK<lastD and lastK<60:

            #plt.Circle((prices["Date"][i],prices["High"][i]),1)
            #plt.bar(prices["Date"][i],1,1.1,bottom=prices["High"][i]*1.01,color='g)
            plt.plot(prices["Date"][i],prices["High"][i]+1,marker="o",ms=4, ls="",color="g") #plot green dot

            greenDotDate.append(i) #store green date
            greenDot.append(prices["High"][i]) #store green dot value

        #Check for Lower Bollinger Band Bounce
        if((lastLow<lastLowBB) or (prices['Low'][i]<prices['LowerBand'][i])) and (prices['Adj Close'][i]>lastClose and prices['Adj Close'][i]>prices['LowerBand'][i]) and lastK<60:
            plt.plot(prices["Date"][i],prices["Low"][i]-1, marker="o", ms=4, ls="", color='b') #plot blue dot
        
        #store values
        lastK=prices['K'][i]
        lastD=prices['D'][i]
        lastLow=prices['Low'][i]
        lastClose=prices['Adj Close'][i]
        lastLowBB=prices['LowerBand'][i]

    #plot moving averages and BBands
    for x in smasUsed: #this for loop calculates the EMAs for the stated periods and appends to dataframe
        sma=x
        prices['SMA_'+str(sma)].plot(label='close')
    prices['UpperBand'].plot(label='close', color='lightgray')
    prices['LowerBand'].plot(label='close', color='lightgray')

    #plot candlesticks
    candlestick_ohlc(ax1,ohlc,width=.5,colorup='k',colordown='r',alpha=0.75)

    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
#change x axis back to datestamps
    ax1.xaxis.set_major_formatter(mticker.MaxNLocator(8)) #add more x axis labels
    plt.tick_params(axis='x',rotation=45) #rotate dates for readability

    #pivot points
    pivots=[] #stores pivot values
    dates=[] #stores dates corresponding to those pivot values
    counter=0 #will keep track of whether a certain value is a pivot
    lastPivot=0 #will store the last Pivot value

    Range=[0,0,0,0,0,0,0,0,0,0] #array used to iterate through stock prices
    dateRange=[0,0,0,0,0,0,0,0,0,0] #array used to iterate through corresponding dates

    for i in prices.index: #iterates through the price history
        currentMax=max(Range,default=0) #determines the maximum value of the 10 item array, identifying a potential pivot
        value=round(prices["High"][i],2) #receives next high value from the dataframe

        Range=Range[1:9] #cuts range array to only the most recent 9 values
        Range.append(value) #adds newest high value to the array
        dateRange=dateRange[1:9] #cuts date array to only the most recent 9 values
        dateRange.append(i) #adds newest date to the array

        if currentMax == max(Range, default=0): #if statement that checks is the max stays the same
            counter+=1 #if yes add 1 to the counter
        else:
            counter=0 #otherwise new potential pivot so reset the counter 
        if counter==5: #checks if we have identified a pivot
            lastPivot=currentMax #assigns last pivot to the current max value
            dateloc=Range.index(lastPivot) #finds index of the Range array that is the last pivot value
            lastDate=dateRange[dateloc] #gets date corresponding to that index
            pivots.append(currentMax) #adds pivot to pivot array
            dates.append(lastDate) #adds pivot to date to date array
    print()

    timeD=dt.timedelta(days=30) #sets length of dotted line on chart

    for index in range(len(pivots)): #iterates through pivot array

        #print(str(pivots[index])+": "+str(dates[index])) #prints Pivot, Date couple
        plt.plot_date([dates[index]-(timeD*0.75), dates[index]+timeD],
#plots horizontal line at pivotal value
                                    [pivots[index],pivots[index]], linestyle="--",
                                    linewidth=1,marker=',')
        plt.annotate(str(pivots[index]), (mdates.date2num(dates[index]), pivots[index]), xytext=(-10,7), textcoords='offset points', fontsize=7, arrowprops=dict(arrowstyle='-|>'))
    
    plt.xlabel('Date') #set x axis label
    plt.ylabel('Price') #set y axis label
    plt.title(stock+" - Daily") #set title
    plt.ylim(prices["Low"].min(), prices["High"].max()*1.05) #add margins

    #plt.yscale("log")

    plt.show()
    #print()
    stock=input("Enter the stock symbol : ") #asks for new stock
