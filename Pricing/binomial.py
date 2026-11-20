import math as m
import numpy as np

def calcBinOption(stockPrice: float, strikePrice: float, riskFree: float, timeTilMature: float, volatility: float, optionType: str, steps: int, american: bool) -> float:
    dt: float = timeTilMature / steps
    u: float = m.exp(volatility * m.sqrt(dt))
    d: float = 1 / u
    p: float = (m.exp(riskFree * dt) - d) / (u - d)
    discount: float = m.exp(-riskFree * dt)

    def payoff(price):
       return np.maximum(price - strikePrice, 0) if optionType == "call" else np.maximum(strikePrice - price, 0)

    j = np.arange(steps + 1)
    values = payoff(stockPrice * u**j * d**(steps - j))

    for i in range(steps - 1, -1, -1):
        values = discount * (p * values[1:i+2] + (1 - p) * values[0:i+1])
        if american:
            j = np.arange(i + 1)
            values = np.maximum(values, payoff(stockPrice * u**j * d**(i - j)))
            
    return values[0]