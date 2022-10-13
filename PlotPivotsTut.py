import yfinance as yf
import datetime as dt
import pandas as pd
from pandas_datareader import data as pdr
import matplotlib.pyplot as plt

yf.pdr_override() #activate yahoo finance workaround
start=dt.datetime(2019,6,1) #sets apart point of dataframe
now=dt.datetime.now() #sets endpoint of dataframe

stock=input("Enter the stock symbol :") #Asks for stock ticker

while stock != "quit": #runs this loop until user enters 'quit' (can do many stocks in a row)
    df=pdr.get_data_yahoo(stock, start, now) #fetches stock price data, saves as data frame

    df["High"].plot(Label="high")

    pivots=[]
    #stock that is local maximum within 10 days, 5 days before to the left and 5 days after to the right
    dates=[]
    counter=0
    lastPivot=0

    Range=[0,0,0,0,0,0,0,0,0,0]
    dateRange=[0,0,0,0,0,0,0,0,0,0]

    for i in df.index:
        currentMax=max(Range, default=0)
        value=round(df["High"][i],2)

        Range=Range[1:9]
        Range.append(value)
        dateRange=dateRange[1:9]
        dateRange.append(i)

        if currentMax==max(Range, default=0): 
            counter+=1 #keep track of how many days straight this current max is the relative max
        else:
            counter=0
        if counter==5:
            lastPivot=currentMax
            dateloc=Range.index(lastPivot)
            lastDate=dateRange[dateloc]

            pivots.append(lastPivot)
            dates.append(lastDate)

    print()

    # print(str(pivots))
    # print(str(dates))
    timeD=dt.timedelta(days=30)

    for index in range(len(pivots)):
        print(str(pivots[index])+": "+str(dates[index]))
        plt.plot_date([dates[index],dates[index]+timeD],
            [pivots[index],pivots[index]], linestyle="-", linewidth=2, marker=",")
            
    plt.show()

    stock=input("Enter the stock symbol :") #asks for new stock