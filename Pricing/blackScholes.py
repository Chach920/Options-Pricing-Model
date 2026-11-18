from math import sqrt, log, exp, pow
from scipy.stats import norm 

def getDs (stockPrice, strikePrice, riskFree, timeTilMature, volatility, ):
    d1 = (log(stockPrice/strikePrice) + (riskFree + pow(volatility, 2)/2) ) / (volatility * sqrt(timeTilMature))
    d2 = d1 - volatility * sqrt(timeTilMature)
    return (d1, d2)

def calculateBlackScholes (stockPrice, strikePrice, riskFree, timeTilMature, volatility, callOrPut):
   d1, d2 = getDs(stockPrice, strikePrice, riskFree, timeTilMature, volatility)
   if callOrPut == "call":
       return (stockPrice * norm(d1) - norm(d2) * strikePrice * exp(-1*riskFree*timeTilMature))
   return(norm(-d2) * strikePrice * exp(-riskFree*timeTilMature)- stockPrice * norm(-d1) )
