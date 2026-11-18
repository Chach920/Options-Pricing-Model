from math import exp
from pytest import approx
from Pricing.blackScholes import calculateBlackScholes

def test_known_textbook_value():
    price = calculateBlackScholes(S=42, K=40, r=0.10,  T=0.5, volatility=0.20, option="call")
    assert price == approx(4.76, abs=0.01)

def test_put_call_parity():
    S, K, r, T, volatility = 100, 95, 0.03, .75, 0.25
    C = calculateBlackScholes(S, K, T, r, volatility, "call")
    P = calculateBlackScholes(S, K, T, r, volatility, "put")
    assert C - P == approx(S - K * exp(-r * T), abs=1e-9)

def test_call_increases_with_volatility():
    low = calculateBlackScholes(100, 100, 0.03, 1, 0.10)
    high = calculateBlackScholes(100, 100, 0.03, 1, 0.40)
    assert high > low