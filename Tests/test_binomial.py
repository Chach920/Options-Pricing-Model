from math import exp

import pytest
from pytest import approx
from Pricing.blackScholes import calculateBlackScholes
from Pricing.binomial import calcBinOption

stockPrice, strikePrice, timeTilMature, riskFree, volatility = 100, 100, 1.0, 0.05, 0.20


def test_one_step_tree_matches_hand_calculation():
    u = exp(0.2)
    d = 1 / u
    p = (exp(0.05) - d) / (u - d)
    expected = exp(-0.05) * (p * (100 * u - 100) + (1 - p) * 0)
    assert calcBinOption(100, 100, 0.05, 1, 0.2, "call", 1, False) == approx(expected)


@pytest.mark.parametrize("option", ["call", "put"])
def test_european_converges_to_black_scholes(option):
    binomialTree = calcBinOption(stockPrice, strikePrice, riskFree, timeTilMature, volatility, option, 2000, False)
    blackScholesPrice = calculateBlackScholes(stockPrice, strikePrice, riskFree, timeTilMature, volatility, option)
    assert binomialTree == approx(blackScholesPrice, abs=0.01)


def test_error_shrinks_with_more_steps():
    blackScholesPrice = calculateBlackScholes(stockPrice, strikePrice, riskFree, timeTilMature, volatility, "call")
    smallStepError = abs(calcBinOption(stockPrice, strikePrice, riskFree, timeTilMature, volatility, "call", 10, False) - blackScholesPrice)
    largeStepError = abs(calcBinOption(stockPrice, strikePrice, riskFree, timeTilMature, volatility, "call", 1000, False) - blackScholesPrice)
    assert largeStepError < smallStepError


def test_american_call_equals_european_call():
    europeanPrice = calcBinOption(stockPrice, strikePrice, riskFree, timeTilMature, volatility, "call", 500, False)
    americanPrice = calcBinOption(stockPrice, strikePrice, riskFree, timeTilMature, volatility, "call", 500, True)
    assert americanPrice == approx(europeanPrice, abs=1e-8)


def test_american_put_at_least_european_put():
    europeanPrice = calcBinOption(stockPrice, strikePrice, riskFree, timeTilMature, volatility, "put", 500, False)
    americanPrice = calcBinOption(stockPrice, strikePrice, riskFree, timeTilMature, volatility, "put", 500, True)
    assert americanPrice >= europeanPrice - 1e-12


def test_american_put_strictly_more_valuable_deep_itm():
    europeanPrice = calcBinOption(50, 100, 0.05, 1, 0.2, "put", 500, False)
    americanPrice = calcBinOption(50, 100, 0.05, 1, 0.2, "put", 500, True)
    assert americanPrice > europeanPrice + 0.01


def test_american_put_at_least_intrinsic():
    americanPrice = calcBinOption(60, 100, 0.05, 1, 0.2, "put", 500, True)
    assert americanPrice >= 100 - 60 - 1e-12


def test_put_call_parity_in_tree():
    callPrice = calcBinOption(stockPrice, strikePrice, riskFree, timeTilMature, volatility, "call", 500, False)
    putPrice = calcBinOption(stockPrice, strikePrice, riskFree, timeTilMature, volatility, "put", 500, False)
    assert callPrice - putPrice == approx(stockPrice - strikePrice * exp(-riskFree * timeTilMature), abs=1e-8)