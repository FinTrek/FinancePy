###############################################################################
# Copyright (C) 2018, 2019, 2020 Dominic O'Kane
###############################################################################

import numpy as np
import time
import matplotlib.pyplot as plt

import sys
sys.path.append("..")

from financepy.utils.date import Date
from financepy.market.curves.discount_curve import DiscountCurve
from financepy.market.curves.discount_curve_flat import DiscountCurveFlat

from financepy.products.bonds.bond import Bond
from financepy.utils.frequency import FrequencyTypes
from financepy.utils.day_count import DayCountTypes
from financepy.utils.global_variables import gDaysInYear
from financepy.products.bonds.bond_option import BondOption
from financepy.utils.FinGlobalTypes import FinOptionTypes
from financepy.models.rates_bdt_tree import FinModelRatesBDT

from FinTestCases import FinTestCases, globalTestCaseMode
testCases = FinTestCases(__file__, globalTestCaseMode)

plotGraphs = False

###############################################################################


def test_BondOption():

    settlement_date = Date(1, 12, 2019)
    issue_date = Date(1, 12, 2018)
    maturity_date = settlement_date.addTenor("10Y")
    coupon = 0.05
    freq_type = FrequencyTypes.SEMI_ANNUAL
    accrual_type = DayCountTypes.ACT_ACT_ICMA
    bond = Bond(issue_date, maturity_date, coupon, freq_type, accrual_type)

    tmat = (maturity_date - settlement_date) / gDaysInYear
    times = np.linspace(0, tmat, 20)
    dates = settlement_date.addYears(times)
    dfs = np.exp(-0.05*times)
    discount_curve = DiscountCurve(settlement_date, dates, dfs)

    expiry_date = settlement_date.addTenor("18m")
    strikePrice = 105.0
    face = 100.0

    ###########################################################################

    strikes = [80, 90, 100, 110, 120]

    optionType = FinOptionTypes.EUROPEAN_CALL

    testCases.header("LABEL", "VALUE")

    price = bond.full_price_from_discount_curve(settlement_date, discount_curve)
    testCases.print("Fixed Income Price:", price)

    numTimeSteps = 100

    testCases.header("OPTION TYPE AND MODEL", "STRIKE", "VALUE")

    for strikePrice in strikes:

        sigma = 0.20

        bondOption = BondOption(bond, expiry_date, strikePrice, face, optionType)
        model = FinModelRatesBDT(sigma, numTimeSteps)
        v = bondOption.value(settlement_date, discount_curve, model)
        testCases.print("EUROPEAN CALL - BK", strikePrice, v)

    for strikePrice in strikes:

        sigma = 0.20

        bondOption = BondOption(bond, expiry_date, strikePrice, face, optionType)
        model = FinModelRatesBDT(sigma, numTimeSteps)
        v = bondOption.value(settlement_date, discount_curve, model)
        testCases.print("EUROPEAN CALL - BK", strikePrice, v)

    ###########################################################################

    optionType = FinOptionTypes.AMERICAN_CALL

    price = bond.full_price_from_discount_curve(settlement_date, discount_curve)
    testCases.header("LABEL", "VALUE")
    testCases.print("Fixed Income Price:", price)

    testCases.header("OPTION TYPE AND MODEL", "STRIKE", "VALUE")

    for strikePrice in strikes:

        sigma = 0.20

        bondOption = BondOption(bond, expiry_date, strikePrice, face, optionType)
        model = FinModelRatesBDT(sigma, numTimeSteps)
        v = bondOption.value(settlement_date, discount_curve, model)
        testCases.print("AMERICAN CALL - BK", strikePrice, v)

    for strikePrice in strikes:

        sigma = 0.20

        bondOption = BondOption(bond, expiry_date, strikePrice, face, optionType)
        model = FinModelRatesBDT(sigma, numTimeSteps)
        v = bondOption.value(settlement_date, discount_curve, model)
        testCases.print("AMERICAN CALL - BK", strikePrice, v)

    ###########################################################################

    optionType = FinOptionTypes.EUROPEAN_PUT

    price = bond.full_price_from_discount_curve(settlement_date, discount_curve)

    for strikePrice in strikes:

        sigma = 0.01

        bondOption = BondOption(bond, expiry_date, strikePrice, face, optionType)
        model = FinModelRatesBDT(sigma, numTimeSteps)
        v = bondOption.value(settlement_date, discount_curve, model)
        testCases.print("EUROPEAN PUT - BK", strikePrice, v)

    for strikePrice in strikes:

        sigma = 0.20

        bondOption = BondOption(bond, expiry_date, strikePrice, face, optionType)
        model = FinModelRatesBDT(sigma, numTimeSteps)
        v = bondOption.value(settlement_date, discount_curve, model)
        testCases.print("EUROPEAN PUT - BK", strikePrice, v)

    ###########################################################################

    optionType = FinOptionTypes.AMERICAN_PUT

    price = bond.full_price_from_discount_curve(settlement_date, discount_curve)

    for strikePrice in strikes:

        sigma = 0.02

        bondOption = BondOption(bond, expiry_date, strikePrice, face, optionType)
        model = FinModelRatesBDT(sigma, numTimeSteps)
        v = bondOption.value(settlement_date, discount_curve, model)
        testCases.print("AMERICAN PUT - BK", strikePrice, v)

    for strikePrice in strikes:

        sigma = 0.20

        bondOption = BondOption(bond, expiry_date, strikePrice, face, optionType)
        model = FinModelRatesBDT(sigma, numTimeSteps)
        v = bondOption.value(settlement_date, discount_curve, model)
        testCases.print("AMERICAN PUT - BK", strikePrice, v)

###############################################################################


def test_BondOptionAmericanConvergenceONE():

    # Build discount curve
    settlement_date = Date(1, 12, 2019)
    discount_curve = DiscountCurveFlat(settlement_date, 0.05)

    # Bond details
    issue_date = Date(1, 9, 2010)
    maturity_date = Date(1, 9, 2025)
    coupon = 0.05
    freq_type = FrequencyTypes.SEMI_ANNUAL
    accrual_type = DayCountTypes.ACT_ACT_ICMA
    bond = Bond(issue_date, maturity_date, coupon, freq_type, accrual_type)

    # Option Details
    expiry_date = Date(1, 12, 2020)
    strikePrice = 100.0
    face = 100.0

    testCases.header("TIME", "N", "PUT_AMER", "PUT_EUR",
                     "CALL_AME", "CALL_EUR")

    timeSteps = range(30, 100, 1)

    for numTimeSteps in timeSteps:

        sigma = 0.20

        start = time.time()

        optionType = FinOptionTypes.AMERICAN_PUT
        bondOption1 = BondOption(bond, expiry_date, strikePrice, face, optionType)
        model = FinModelRatesBDT(sigma, numTimeSteps)
        v1put = bondOption1.value(settlement_date, discount_curve, model)

        optionType = FinOptionTypes.EUROPEAN_PUT
        bondOption2 = BondOption(bond, expiry_date, strikePrice, face, optionType)
        model = FinModelRatesBDT(sigma, numTimeSteps)
        v2put = bondOption2.value(settlement_date, discount_curve, model)

        optionType = FinOptionTypes.AMERICAN_CALL
        bondOption1 = BondOption(bond, expiry_date, strikePrice, face, optionType)
        model = FinModelRatesBDT(sigma, numTimeSteps)
        v1call = bondOption1.value(settlement_date, discount_curve, model)

        optionType = FinOptionTypes.EUROPEAN_CALL
        bondOption2 = BondOption(bond, expiry_date, strikePrice, face, optionType)
        model = FinModelRatesBDT(sigma, numTimeSteps)
        v2call = bondOption2.value(settlement_date, discount_curve, model)

        end = time.time()

        period = end - start

        testCases.print(period, numTimeSteps, v1put, v2put, v1call, v2call)

###############################################################################


def test_BondOptionAmericanConvergenceTWO():

    # Build discount curve
    settlement_date = Date(1, 12, 2019)
    discount_curve = DiscountCurveFlat(settlement_date,
                                       0.05,
                                       FrequencyTypes.CONTINUOUS)

    # Bond details
    issue_date = Date(1, 9, 2014)
    maturity_date = Date(1, 9, 2025)
    coupon = 0.05
    freq_type = FrequencyTypes.ANNUAL
    accrual_type = DayCountTypes.ACT_ACT_ICMA
    bond = Bond(issue_date, maturity_date, coupon, freq_type, accrual_type)
    expiry_date = settlement_date.addTenor("18m")
    face = 100.0

    spotValue = bond.full_price_from_discount_curve(settlement_date, discount_curve)
    testCases.header("LABEL", "VALUE")
    testCases.print("BOND PRICE", spotValue)

    testCases.header("TIME", "N", "EUR_CALL", "AMER_CALL",
                     "EUR_PUT", "AMER_PUT")

    sigma = 0.2
    model = FinModelRatesBDT(sigma)
    K = 101.0

    vec_ec = []
    vec_ac = []
    vec_ep = []
    vec_ap = []

    if 1 == 1:
        K = 100.0
        bkModel = FinModelRatesBDT(sigma, 100)
        europeanCallBondOption = BondOption(bond, expiry_date, K, face,
                                            FinOptionTypes.EUROPEAN_CALL)

        v_ec = europeanCallBondOption.value(settlement_date, discount_curve,
                                            model)
        testCases.header("LABEL", "VALUE")
        testCases.print("OPTION", v_ec)

    num_stepsVector = range(100, 100, 1)  # should be 100-400

    for num_steps in num_stepsVector:

        bkModel = FinModelRatesBDT(sigma, num_steps)

        start = time.time()

        europeanCallBondOption = BondOption(bond, expiry_date, K, face,
                                            FinOptionTypes.EUROPEAN_CALL)
        v_ec = europeanCallBondOption.value(settlement_date, discount_curve,
                                            bkModel)

        americanCallBondOption = BondOption(bond, expiry_date, K, face,
                                            FinOptionTypes.AMERICAN_CALL)
        v_ac = americanCallBondOption.value(settlement_date, discount_curve,
                                            bkModel)

        europeanPutBondOption = BondOption(bond, expiry_date, K, face,
                                           FinOptionTypes.EUROPEAN_PUT)
        v_ep = europeanPutBondOption.value(settlement_date, discount_curve,
                                           bkModel)

        americanPutBondOption = BondOption(bond, expiry_date, K, face,
                                           FinOptionTypes.AMERICAN_PUT)
        v_ap = americanPutBondOption.value(settlement_date, discount_curve,
                                           bkModel)

        end = time.time()
        period = end - start

        testCases.print(period, num_steps, v_ec, v_ac, v_ep, v_ap)

        vec_ec.append(v_ec)
        vec_ac.append(v_ac)
        vec_ep.append(v_ep)
        vec_ap.append(v_ap)

    if plotGraphs:

        plt.figure()
        plt.plot(num_stepsVector, vec_ec, label="European Call")
        plt.legend()

        plt.figure()
        plt.plot(num_stepsVector, vec_ac, label="American Call")
        plt.legend()

        plt.figure()
        plt.plot(num_stepsVector, vec_ep, label="European Put")
        plt.legend()

        plt.figure()
        plt.plot(num_stepsVector, vec_ap, label="American Put")
        plt.legend()

###############################################################################
###############################################################################

def test_BondOptionZEROVOLConvergence():

    # Build discount curve
    settlement_date = Date(1, 12, 2019) # CHANGED
    rate = 0.05
    discount_curve = DiscountCurveFlat(settlement_date, rate, FrequencyTypes.ANNUAL)

    # Bond details
    issue_date = Date(1, 9, 2015)
    maturity_date = Date(1, 9, 2025)
    coupon = 0.06
    freq_type = FrequencyTypes.ANNUAL
    accrual_type = DayCountTypes.ACT_ACT_ICMA
    bond = Bond(issue_date, maturity_date, coupon, freq_type, accrual_type)

    # Option Details
    expiry_date = settlement_date.addTenor("18m") # FinDate(1, 12, 2021)
#    print("EXPIRY:", expiry_date)
    face = 100.0

    dfExpiry = discount_curve.df(expiry_date)
    spotCleanValue = bond.clean_price_from_discount_curve(settlement_date, discount_curve)
    fwdCleanValue = bond.clean_price_from_discount_curve(expiry_date, discount_curve)
#    print("BOND SpotCleanBondPx", spotCleanValue)
#    print("BOND FwdCleanBondPx", fwdCleanValue)
#    print("BOND Accrued:", bond._accruedInterest)

    spotCleanValue = bond.clean_price_from_discount_curve(settlement_date, discount_curve)

    testCases.header("STRIKE", "STEPS",
                     "CALL_INT", "CALL_INT_PV", "CALL_EUR", "CALL_AMER",
                     "PUT_INT", "PUT_INT_PV", "PUT_EUR", "PUT_AMER") 

    numTimeSteps = range(100, 1000, 200)
    strikePrices = [90, 100, 110, 120]

    for strikePrice in strikePrices:
        
        callIntrinsic = max(spotCleanValue - strikePrice, 0)
        putIntrinsic = max(strikePrice - spotCleanValue, 0)
        callIntrinsicPV = max(fwdCleanValue - strikePrice, 0) * dfExpiry
        putIntrinsicPV = max(strikePrice - fwdCleanValue, 0) * dfExpiry

        for num_steps in numTimeSteps:

            sigma = 0.0000001
            model = FinModelRatesBDT(sigma, num_steps)
        
            optionType = FinOptionTypes.EUROPEAN_CALL
            bondOption1 = BondOption(bond, expiry_date, strikePrice, face, optionType)
            v1 = bondOption1.value(settlement_date, discount_curve, model)

            optionType = FinOptionTypes.AMERICAN_CALL
            bondOption2 = BondOption(bond, expiry_date, strikePrice, face, optionType)
            v2 = bondOption2.value(settlement_date, discount_curve, model)

            optionType = FinOptionTypes.EUROPEAN_PUT
            bondOption3 = BondOption(bond, expiry_date, strikePrice, face, optionType)
            v3 = bondOption3.value(settlement_date, discount_curve, model)
        
            optionType = FinOptionTypes.AMERICAN_PUT
            bondOption4 = BondOption(bond, expiry_date, strikePrice, face, optionType)
            v4 = bondOption4.value(settlement_date, discount_curve, model)
        
            testCases.print(strikePrice, num_steps,
                            callIntrinsic, callIntrinsicPV, v1, v2,
                            putIntrinsic, putIntrinsicPV, v3, v4)

###############################################################################

test_BondOptionZEROVOLConvergence()
test_BondOption()
# test_BondOptionAmericanConvergenceONE()
test_BondOptionAmericanConvergenceTWO()
testCases.compareTestCases()
