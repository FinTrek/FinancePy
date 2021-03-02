###############################################################################
# Copyright (C) 2018, 2019, 2020 Dominic O'Kane
###############################################################################

import time

import sys
sys.path.append("..")

from financepy.utils.FinGlobalTypes import FinOptionTypes
from financepy.products.equity.FinEquityVanillaOptionOLD import FinEquityVanillaOptionOLD
from financepy.market.curves.FinDiscountCurveFlat import FinDiscountCurveFlat
from financepy.models.FinModelBlackScholes import FinModelBlackScholes
from financepy.utils.Date import Date

from FinTestCases import FinTestCases, globalTestCaseMode
testCases = FinTestCases(__file__, globalTestCaseMode)

###############################################################################


def test_FinEquityVanillaOptionFactored():

    valuation_date = Date(1, 1, 2015)
    expiry_date = Date(1, 7, 2015)
    stockPrice = 100
    volatility = 0.30
    interestRate = 0.05
    dividendYield = 0.01
    model = FinModelBlackScholes(volatility)
    discount_curve = FinDiscountCurveFlat(valuation_date, interestRate)

    numPathsList = [10000, 20000, 40000, 80000, 160000, 320000]

    testCases.header("NUMPATHS", "VALUE_BS", "VALUE_MC", "TIME")

    for numPaths in numPathsList:

        callOption = FinEquityVanillaOptionOLD(
            expiry_date, 100.0, FinOptionTypes.EUROPEAN_CALL)
        value = callOption.value(valuation_date, stockPrice, discount_curve,
                                 dividendYield, model)
        start = time.time()
        valueMC = callOption.valueMC(valuation_date, stockPrice, discount_curve,
                                     dividendYield, model, numPaths)
        end = time.time()
        duration = end - start
        testCases.print(numPaths, value, valueMC, duration)


###############################################################################

    stockPrices = range(80, 120, 10)
    numPaths = 100000

    testCases.header("NUMPATHS", "CALL_VALUE_BS", "CALL_VALUE_MC", 
                     "CALL_VALUE_MC_SOBOL", "TIME")
    useSobol = True

    for stockPrice in stockPrices:

        callOption = FinEquityVanillaOptionOLD(expiry_date, 100.0, 
                                            FinOptionTypes.EUROPEAN_CALL)

        value = callOption.value(valuation_date, stockPrice, discount_curve,
                                 dividendYield, model)

        start = time.time()

        useSobol = False
        valueMC1 = callOption.valueMC(valuation_date, stockPrice, discount_curve,
                                      dividendYield, model, numPaths, useSobol)

        useSobol = True
        valueMC2 = callOption.valueMC(valuation_date, stockPrice, discount_curve,
                                      dividendYield, model, numPaths, useSobol)

        end = time.time()
        duration = end - start
        testCases.print(numPaths, value, valueMC1, valueMC2, duration)

###############################################################################

    stockPrices = range(80, 120, 10)
    numPaths = 100000

    testCases.header("NUMPATHS", "PUT_VALUE_BS", "PUT_VALUE_MC", 
                     "PUT_VALUE_MC_SOBOL", "TIME")

    for stockPrice in stockPrices:

        putOption = FinEquityVanillaOptionOLD(expiry_date, 100.0, 
                                           FinOptionTypes.EUROPEAN_PUT)

        value = putOption.value(valuation_date, stockPrice, discount_curve,
                                dividendYield, model)

        start = time.time()

        useSobol = False
        valueMC1 = putOption.valueMC(valuation_date, stockPrice, discount_curve,
                                      dividendYield, model, numPaths, useSobol)

        useSobol = True
        valueMC2 = putOption.valueMC(valuation_date, stockPrice, discount_curve,
                                      dividendYield, model, numPaths, useSobol)

        end = time.time()
        duration = end - start
        testCases.print(numPaths, value, valueMC1, valueMC2, duration)

###############################################################################

    stockPrices = range(80, 120, 10)

    testCases.header("STOCK PRICE", "CALL_VALUE_BS", "CALL_DELTA_BS", 
                     "CALL_VEGA_BS", "CALL_THETA_BS", "CALL_RHO_BS")

    for stockPrice in stockPrices:

        callOption = FinEquityVanillaOptionOLD(expiry_date, 100.0, 
                                            FinOptionTypes.EUROPEAN_CALL)
        value = callOption.value(valuation_date, stockPrice, discount_curve,
                                 dividendYield, model)
        delta = callOption.delta(valuation_date, stockPrice, discount_curve,
                                 dividendYield, model)
        vega = callOption.vega(valuation_date, stockPrice, discount_curve,
                                 dividendYield, model)
        theta = callOption.theta(valuation_date, stockPrice, discount_curve,
                                 dividendYield, model)
        rho = callOption.rho(valuation_date, stockPrice, discount_curve,
                                 dividendYield, model)
        testCases.print(stockPrice, value, delta, vega, theta, rho)

    ###########################################################################

    testCases.header("STOCK PRICE", "PUT_VALUE_BS", "PUT_DELTA_BS", 
                     "PUT_VEGA_BS", "PUT_THETA_BS", "PUT_RHO_BS")

    for stockPrice in stockPrices:
        
        putOption = FinEquityVanillaOptionOLD(expiry_date, 100.0, 
                                           FinOptionTypes.EUROPEAN_PUT)

        value = putOption.value(valuation_date, stockPrice, discount_curve,
                                 dividendYield, model)
        delta = putOption.delta(valuation_date, stockPrice, discount_curve,
                                 dividendYield, model)
        vega = putOption.vega(valuation_date, stockPrice, discount_curve,
                                 dividendYield, model)
        theta = putOption.theta(valuation_date, stockPrice, discount_curve,
                                 dividendYield, model)
        rho = putOption.rho(valuation_date, stockPrice, discount_curve,
                                 dividendYield, model)
        testCases.print(stockPrice, value, delta, vega, theta, rho)

###############################################################################

    testCases.header("STOCK PRICE", "VALUE_BS", "VOL_IN", "IMPLD_VOL")

    stockPrices = range(60, 150, 10)

    for stockPrice in stockPrices:
        callOption = FinEquityVanillaOptionOLD(
            expiry_date, 100.0, FinOptionTypes.EUROPEAN_CALL)
        value = callOption.value(
            valuation_date,
            stockPrice,
            discount_curve,
            dividendYield,
            model)
        impliedVol = callOption.impliedVolatility(
            valuation_date, stockPrice, discount_curve, dividendYield, value)
        testCases.print(stockPrice, value, volatility, impliedVol)

###############################################################################


test_FinEquityVanillaOptionFactored()
testCases.compareTestCases()
