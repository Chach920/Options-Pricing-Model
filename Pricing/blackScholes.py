from math import sqrt, log, exp, pow
from scipy.stats import norm 

def getDs (stockPrice, strikePrice, riskFree, timeTilMature, volatility, ) -> float:
    d1: float = (log(stockPrice/strikePrice) + (riskFree + pow(volatility, 2)/2) ) / (volatility * sqrt(timeTilMature))
    d2: float = d1 - volatility * sqrt(timeTilMature)
    return (d1, d2)

def calculateBlackScholes (stockPrice, strikePrice, riskFree, timeTilMature, volatility, optionType: str) -> float:
   d1: float; d2: float = getDs(stockPrice, strikePrice, riskFree, timeTilMature, volatility)
   try:
       if optionType == "call" or optionType == "put":
           if optionType == "call":
               return (stockPrice * norm(d1) - norm(d2) * strikePrice * exp(-1*riskFree*timeTilMature))
           else:
                return(norm(-d2) * strikePrice * exp(-riskFree*timeTilMature)- stockPrice * norm(-d1) )
   except:
       print("Error: Invalid option type. Please use 'call' or 'put'.")
