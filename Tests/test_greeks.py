import Pricing.greeks
import Pricing.blackScholes

def testAgainstFormula (stockPrice, strikePrice, riskFree, timeTilMature, volatility, option):
    price: float = Pricing.blackScholes.calculateBlackScholes(stockPrice, strikePrice, riskFree, timeTilMature, volatility, option)
    delta: float = Pricing.greeks.calculateDelta(stockPrice, strikePrice, riskFree, timeTilMature, volatility, option)
    gamma: float = Pricing.greeks.calculateGamma(stockPrice, strikePrice, riskFree, timeTilMature, volatility)
    vega: float = Pricing.greeks.calculateVega(stockPrice, strikePrice, riskFree, timeTilMature, volatility)
    theta: float = Pricing.greeks.calculateTheta(stockPrice, strikePrice, riskFree, timeTilMature, volatility, option)
    rho: float = Pricing.greeks.calculateRho(stockPrice, strikePrice, riskFree, timeTilMature, volatility, option)
    priceViaGreeks: float = price + delta * stockPrice + 0.5 * gamma * (stockPrice ** 2) * (volatility ** 2) * timeTilMature + vega * volatility + theta * timeTilMature + rho * riskFree

    assert price == pytest.approx(priceViaGreeks)

def testIdentityDelta(stockprice:float, strikePrice: float, riskFree: float, timeTilMature: float, volatility: float, option: str):
    deltaCall: float = Pricing.greeks.calculateDelta(stockprice, strikePrice, riskFree, timeTilMature, volatility, "call")
    deltaPut: float = Pricing.greeks.calculateDelta(stockprice, strikePrice, riskFree, timeTilMature, volatility, "put")

    assert (deltaCall == deltaPut +1)

def testidentityGamma(stockprice:float, strikePrice: float, riskFree: float, timeTilMature: float, volatility: float):
    gammaCall: float = Pricing.greeks.calculateGamma(stockprice, strikePrice, riskFree, timeTilMature, volatility)
    gammaPut: float = Pricing.greeks.calculateGamma(stockprice, strikePrice, riskFree, timeTilMature, volatility)

    assert (gammaCall == gammaPut)