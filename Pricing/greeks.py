import math
from scipy.stats import norm
import Pricing.blackScholes

def calculateDelta(stockPrice: float, strikePrice: float, riskFree: float, timeTilMature: float, volatility: float, option: str) -> float:
    d1: float = (math.log(stockPrice/strikePrice) + (riskFree + pow(volatility, 2)/2) ) / (volatility * math.sqrt(timeTilMature))
    try:
        if option == "call" or option == "put":
            if option == "call":
                return norm(d1)
            else:
                return norm(d1) - 1
    except:
        print("Error: Invalid option type. Please use 'call' or 'put'.")

def calculateGamma(stockPrice: float, strikePrice: float, riskFree: float, timeTilMature: float, volatility: float) -> float:
    d1: float = (math.log(stockPrice/strikePrice) + (riskFree + pow(volatility, 2)/2) ) / (volatility * math.sqrt(timeTilMature))
    return norm.pdf(d1) / (stockPrice * volatility * math.sqrt(timeTilMature))

def calculateVega(stockPrice: float, strikePrice: float, riskFree: float, timeTilMature: float, volatility: float) -> float:
    d1: float = (math.log(stockPrice/strikePrice) + (riskFree + pow(volatility, 2)/2) ) / (volatility * math.sqrt(timeTilMature))
    return stockPrice * norm.pdf(d1) * math.sqrt(timeTilMature)

def calculateTheta(stockPrice: float, strikePrice: float, riskFree: float, timeTilMature: float, volatility: float, option: str) -> float:
    d1:float; d2: float = Pricing.blackScholes.getDs(stockPrice, strikePrice, riskFree, timeTilMature, volatility)
    try:
        if option == "call" or option == "put":
            if option == "call":
                return (-stockPrice * norm.pdf(d1) * volatility / (2 * math.sqrt(timeTilMature)) - riskFree * strikePrice * math.exp(-riskFree * timeTilMature) * norm(d2))
            else:
                return (-stockPrice * norm.pdf(d1) * volatility / (2 * math.sqrt(timeTilMature)) + riskFree * strikePrice * math.exp(-riskFree * timeTilMature) * norm(-d2))
    except:
        print("Error: Invalid option type. Please use 'call' or 'put'.")

def calculateRho(stockPrice: float, strikePrice: float, riskFree: float, timeTilMature: float, volatility: float, option: str) -> float:
    d1:float; d2: float = Pricing.blackScholes.getDs(stockPrice, strikePrice, riskFree, timeTilMature, volatility)
    try:
        if option == "call" or option == "put":
            if option == "call":
                return strikePrice * timeTilMature * math.exp(-riskFree * timeTilMature) * norm(d2)
            else:
                return -strikePrice * timeTilMature * math.exp(-riskFree * timeTilMature) * norm(-d2)
    except:
        print("Error: Invalid option type. Please use 'call' or 'put'.")

def bsWithGreeks(stockPrice: float, strikePrice: float, riskFree: float, timeTilMature: float, volatility: float, option: str) -> dict:
    price: float = Pricing.blackScholes.calculateBlackScholes(stockPrice, strikePrice, riskFree, timeTilMature, volatility, option)
    delta: float = calculateDelta(stockPrice, strikePrice, riskFree, timeTilMature, volatility, option)
    gamma: float = calculateGamma(stockPrice, strikePrice, riskFree, timeTilMature, volatility)
    vega: float = calculateVega(stockPrice, strikePrice, riskFree, timeTilMature, volatility)
    theta: float = calculateTheta(stockPrice, strikePrice, riskFree, timeTilMature, volatility, option)
    rho: float = calculateRho(stockPrice, strikePrice, riskFree, timeTilMature, volatility, option)
    priceViaGreeks: float = price + delta * stockPrice + 0.5 * gamma * (stockPrice ** 2) * (volatility ** 2) * timeTilMature + vega * volatility + theta * timeTilMature + rho * riskFree

    return {
        "price": price,
        "delta": delta,
        "gamma": gamma,
        "vega": vega,
        "theta": theta,
        "rho": rho,
        "priceViaGreeks": priceViaGreeks
    }