###############################################################################
# Copyright (C) 2018, 2019, 2020 Dominic O'Kane
###############################################################################

import time

import sys
sys.path.append("..")

from financepy.products.equity.FinEquityFloatLookbackOption import FinEquityFloatLookbackOption
from financepy.products.equity.FinEquityFixedLookbackOption import FinEquityFixedLookbackOption
from financepy.utils.FinGlobalTypes import FinOptionTypes
from financepy.market.curves.FinDiscountCurveFlat import FinDiscountCurveFlat
from financepy.utils.Date import Date

from FinTestCases import FinTestCases, globalTestCaseMode
testCases = FinTestCases(__file__, globalTestCaseMode)

###############################################################################

def test_FinEquityLookBackOption():
    valuation_date = Date(1, 1, 2015)
    expiry_date = Date(1, 1, 2016)
    stockPrice = 100.0
    volatility = 0.3
    interestRate = 0.05
    dividendYield = 0.01
    numPathsRange = [10000]
    stockPriceRange = range(90, 110, 10)
    num_steps_per_year = 252

    discount_curve = FinDiscountCurveFlat(valuation_date, interestRate)
    dividendCurve = FinDiscountCurveFlat(valuation_date, dividendYield)

###############################################################################

    testCases.header(
        "NUMPATHS",
        "OPTION_TYPE",
        "S",
        "SMIN",
        "VALUE",
        "VALUE_MC",
        "DIFF",
        "TIME")

    optionType = FinOptionTypes.EUROPEAN_CALL
    for stockPrice in stockPriceRange:
        for numPaths in numPathsRange:
            option = FinEquityFloatLookbackOption(expiry_date, optionType)
            stockMin = stockPrice
            value = option.value(
                valuation_date,
                stockPrice,
                discount_curve,
                dividendCurve,
                volatility,
                stockMin)
            start = time.time()
            valueMC = option.valueMC(
                valuation_date,
                stockPrice,
                discount_curve,
                dividendCurve,
                volatility,
                stockMin,
                numPaths,
                num_steps_per_year)
            end = time.time()
            timeElapsed = round(end - start, 3)
            diff = valueMC - value
            testCases.print(
                numPaths,
                optionType,
                stockPrice,
                stockMin,
                value,
                valueMC,
                diff,
                timeElapsed)

    testCases.header(
        "NUMPATHS",
        "OPTION_TYPE",
        "S",
        "SMIN",
        "VALUE",
        "VALUE_MC",
        "DIFF",
        "TIME")

    optionType = FinOptionTypes.EUROPEAN_CALL
    for stockPrice in stockPriceRange:
        for numPaths in numPathsRange:
            option = FinEquityFloatLookbackOption(expiry_date, optionType)
            stockMin = stockPrice - 10
            value = option.value(
                valuation_date,
                stockPrice,
                discount_curve,
                dividendCurve,
                volatility,
                stockMin)
            start = time.time()
            valueMC = option.valueMC(
                valuation_date,
                stockPrice,
                discount_curve,
                dividendCurve,
                volatility,
                stockMin,
                numPaths,
                num_steps_per_year)
            end = time.time()
            timeElapsed = round(end - start, 3)
            diff = valueMC - value
            testCases.print(
                numPaths,
                optionType,
                stockPrice,
                stockMin,
                value,
                valueMC,
                diff,
                timeElapsed)

    testCases.header(
        "NUMPATHS",
        "OPTION_TYPE",
        "S",
        "SMAX",
        "VALUE",
        "VALUE_MC",
        "DIFF",
        "TIME")

    optionType = FinOptionTypes.EUROPEAN_PUT
    for stockPrice in stockPriceRange:
        for numPaths in numPathsRange:
            option = FinEquityFloatLookbackOption(expiry_date, optionType)
            stockMax = stockPrice
            value = option.value(
                valuation_date,
                stockPrice,
                discount_curve,
                dividendCurve,
                volatility,
                stockMax)
            start = time.time()
            valueMC = option.valueMC(
                valuation_date,
                stockPrice,
                discount_curve,
                dividendCurve,
                volatility,
                stockMax,
                numPaths,
                num_steps_per_year)
            end = time.time()
            timeElapsed = round(end - start, 3)
            diff = valueMC - value
            testCases.print(
                numPaths,
                optionType,
                stockPrice,
                stockMax,
                value,
                valueMC,
                diff,
                timeElapsed)

    testCases.header(
        "NUMPATHS",
        "OPTION_TYPE",
        "S",
        "SMAX",
        "VALUE",
        "VALUE_MC",
        "DIFF",
        "TIME")

    optionType = FinOptionTypes.EUROPEAN_PUT
    for stockPrice in stockPriceRange:
        for numPaths in numPathsRange:
            option = FinEquityFloatLookbackOption(expiry_date, optionType)
            stockMax = stockPrice + 10
            value = option.value(
                valuation_date,
                stockPrice,
                discount_curve,
                dividendCurve,
                volatility,
                stockMax)
            start = time.time()
            valueMC = option.valueMC(
                valuation_date,
                stockPrice,
                discount_curve,
                dividendCurve,
                volatility,
                stockMax,
                numPaths,
                num_steps_per_year)
            end = time.time()
            timeElapsed = round(end - start, 3)
            diff = valueMC - value
            testCases.print(
                numPaths,
                optionType,
                stockPrice,
                stockMax,
                value,
                valueMC,
                diff,
                timeElapsed)

###############################################################################
###############################################################################

    stockPriceRange = range(90, 110, 10)
    num_steps_per_year = 252

    testCases.header(
        "NUMPATHS",
        "OPTION_TYPE",
        "S",
        "K",
        "SMAX",
        "VALUE",
        "VALUE_MC",
        "DIFF",
        "TIME")

    optionType = FinOptionTypes.EUROPEAN_CALL
    k = 95.0
    for stockPrice in stockPriceRange:
        for numPaths in numPathsRange:
            option = FinEquityFixedLookbackOption(expiry_date, optionType, k)
            stockMax = stockPrice
            value = option.value(
                valuation_date,
                stockPrice,
                discount_curve,
                dividendCurve,
                volatility,
                stockMax)
            start = time.time()
            valueMC = option.valueMC(
                valuation_date,
                stockPrice,
                discount_curve,
                dividendCurve,
                volatility,
                stockMax,
                numPaths,
                num_steps_per_year)
            end = time.time()
            timeElapsed = round(end - start, 3)
            diff = valueMC - value
            testCases.print(
                numPaths,
                optionType,
                stockPrice,
                k,
                stockMax,
                value,
                valueMC,
                diff,
                timeElapsed)

    testCases.header(
        "NUMPATHS",
        "OPTION_TYPE",
        "S",
        "K",
        "SMAX",
        "VALUE",
        "VALUE_MC",
        "DIFF",
        "TIME")

    optionType = FinOptionTypes.EUROPEAN_CALL
    k = 100.0
    for stockPrice in stockPriceRange:
        for numPaths in numPathsRange:
            option = FinEquityFixedLookbackOption(expiry_date, optionType, k)
            stockMax = stockPrice
            value = option.value(
                valuation_date,
                stockPrice,
                discount_curve,
                dividendCurve,
                volatility,
                stockMax)
            start = time.time()
            valueMC = option.valueMC(
                valuation_date,
                stockPrice,
                discount_curve,
                dividendCurve,
                volatility,
                stockMax,
                numPaths,
                num_steps_per_year)
            end = time.time()
            timeElapsed = round(end - start, 3)
            diff = valueMC - value
            testCases.print(
                numPaths,
                optionType,
                stockPrice,
                k,
                stockMax,
                value,
                valueMC,
                diff,
                timeElapsed)

    testCases.header(
        "NUMPATHS",
        "OPTION_TYPE",
        "S",
        "K",
        "SMAX",
        "VALUE",
        "VALUE_MC",
        "DIFF",
        "TIME")

    optionType = FinOptionTypes.EUROPEAN_CALL
    k = 105.0
    for stockPrice in stockPriceRange:
        for numPaths in numPathsRange:
            option = FinEquityFixedLookbackOption(expiry_date, optionType, k)
            stockMax = stockPrice + 10.0
            value = option.value(
                valuation_date,
                stockPrice,
                discount_curve,
                dividendCurve,
                volatility,
                stockMax)
            start = time.time()
            valueMC = option.valueMC(
                valuation_date,
                stockPrice,
                discount_curve,
                dividendCurve,
                volatility,
                stockMax,
                numPaths,
                num_steps_per_year)
            end = time.time()
            timeElapsed = round(end - start, 3)
            diff = valueMC - value
            testCases.print(
                numPaths,
                optionType,
                stockPrice,
                k,
                stockMax,
                value,
                valueMC,
                diff,
                timeElapsed)

    testCases.header(
        "NUMPATHS",
        "OPTION_TYPE",
        "S",
        "K",
        "SMIN",
        "VALUE",
        "VALUE_MC",
        "DIFF",
        "TIME")

    optionType = FinOptionTypes.EUROPEAN_PUT
    k = 95.0
    for stockPrice in stockPriceRange:
        for numPaths in numPathsRange:
            option = FinEquityFixedLookbackOption(expiry_date, optionType, k)
            stockMin = stockPrice
            value = option.value(
                valuation_date,
                stockPrice,
                discount_curve,
                dividendCurve,
                volatility,
                stockMin)
            start = time.time()
            valueMC = option.valueMC(
                valuation_date,
                stockPrice,
                discount_curve,
                dividendCurve,
                volatility,
                stockMin,
                numPaths,
                num_steps_per_year)
            end = time.time()
            timeElapsed = round(end - start, 3)
            diff = valueMC - value
            testCases.print(
                numPaths,
                optionType,
                stockPrice,
                k,
                stockMin,
                value,
                valueMC,
                diff,
                timeElapsed)

    testCases.header(
        "NUMPATHS",
        "OPTION_TYPE",
        "S",
        "K",
        "SMIN",
        "VALUE",
        "VALUE_MC",
        "DIFF",
        "TIME")

    optionType = FinOptionTypes.EUROPEAN_PUT
    k = 100.0
    for stockPrice in stockPriceRange:
        for numPaths in numPathsRange:
            option = FinEquityFixedLookbackOption(expiry_date, optionType, k)
            stockMin = stockPrice
            value = option.value(
                valuation_date,
                stockPrice,
                discount_curve,
                dividendCurve,
                volatility,
                stockMin)
            start = time.time()
            valueMC = option.valueMC(
                valuation_date,
                stockPrice,
                discount_curve,
                dividendCurve,
                volatility,
                stockMin,
                numPaths,
                num_steps_per_year)
            end = time.time()
            timeElapsed = round(end - start, 3)
            diff = valueMC - value
            testCases.print(
                numPaths,
                optionType,
                stockPrice,
                k,
                stockMin,
                value,
                valueMC,
                diff,
                timeElapsed)

    testCases.header(
        "NUMPATHS",
        "OPTION_TYPE",
        "S",
        "K",
        "SMIN",
        "VALUE",
        "VALUE_MC",
        "DIFF",
        "TIME")

    optionType = FinOptionTypes.EUROPEAN_PUT
    k = 105.0
    for stockPrice in stockPriceRange:
        for numPaths in numPathsRange:
            option = FinEquityFixedLookbackOption(expiry_date, optionType, k)
            stockMin = stockPrice - 10.0
            value = option.value(
                valuation_date,
                stockPrice,
                discount_curve,
                dividendCurve,
                volatility,
                stockMin)
            start = time.time()
            valueMC = option.valueMC(
                valuation_date,
                stockPrice,
                discount_curve,
                dividendCurve,
                volatility,
                stockMin,
                numPaths,
                num_steps_per_year)
            end = time.time()
            timeElapsed = round(end - start, 3)
            diff = valueMC - value
            testCases.print(
                numPaths,
                optionType,
                stockPrice,
                k,
                stockMin,
                value,
                valueMC,
                diff,
                timeElapsed)

###############################################################################

def test_example():

    expiry_date = Date(1, 1, 2021)
    strikePrice = 105.0
    optionTypeCall = FinOptionTypes.EUROPEAN_CALL
    optionTypePut = FinOptionTypes.EUROPEAN_PUT
    lookbackCall = FinEquityFixedLookbackOption(expiry_date, optionTypeCall, strikePrice)
    lookbackPut = FinEquityFixedLookbackOption(expiry_date, optionTypePut, strikePrice)

    valuation_date = Date(1, 1, 2020)
    interestRate = 0.10
    stockPrice = 100.0
    dividendYield = 0.0
    stockMinMax = 100.0

    discount_curve = FinDiscountCurveFlat(valuation_date, interestRate)
    dividendCurve = FinDiscountCurveFlat(valuation_date, dividendYield)

    volatilities = [0.30]

    testCases.header("VALUE")
    for vol in volatilities:
        v = lookbackCall.value(valuation_date, stockPrice, discount_curve, dividendCurve, vol, stockMinMax)
        testCases.print(v)

###############################################################################

test_example()
#test_FinEquityLookBackOption()
testCases.compareTestCases()
