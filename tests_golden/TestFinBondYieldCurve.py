###############################################################################
# Copyright (C) 2018, 2019, 2020 Dominic O'Kane
###############################################################################

import datetime as dt
import os

import sys
sys.path.append("..")

from financepy.utils.frequency import FrequencyTypes
from financepy.utils.day_count import DayCountTypes
from financepy.utils.date import Date, fromDatetime
from financepy.products.bonds.bond import Bond
from financepy.products.bonds.yield_curve import BondYieldCurve
from financepy.products.bonds.yield_curve_model import *

from FinTestCases import FinTestCases, globalTestCaseMode
testCases = FinTestCases(__file__, globalTestCaseMode)

###############################################################################
###############################################################################


def test_BondYieldCurve():

    ###########################################################################

    import pandas as pd
    path = os.path.join(os.path.dirname(__file__), './data/giltBondPrices.txt')
    bondDataFrame = pd.read_csv(path, sep='\t')
    bondDataFrame['mid'] = 0.5*(bondDataFrame['bid'] + bondDataFrame['ask'])

    freq_type = FrequencyTypes.SEMI_ANNUAL
    accrual_type = DayCountTypes.ACT_ACT_ICMA
    settlement = Date(19, 9, 2012)

    bonds = []
    ylds = []

    for _, bond in bondDataFrame.iterrows():

        dateString = bond['maturity']
        matDatetime = dt.datetime.strptime(dateString, '%d-%b-%y')
        maturityDt = fromDatetime(matDatetime)
        issueDt = Date(maturityDt._d, maturityDt._m, 2000)
        coupon = bond['coupon']/100.0
        clean_price = bond['mid']
        bond = Bond(issueDt, maturityDt, coupon, freq_type, accrual_type)
        yld = bond.yield_to_maturity(settlement, clean_price)
        bonds.append(bond)
        ylds.append(yld)

###############################################################################

    curveFitMethod = CurveFitPolynomial()
    fittedCurve1 = BondYieldCurve(settlement, bonds, ylds, curveFitMethod)
#    fittedCurve1.display("GBP Yield Curve")

    curveFitMethod = CurveFitPolynomial(5)
    fittedCurve2 = BondYieldCurve(settlement, bonds, ylds, curveFitMethod)
#    fittedCurve2.display("GBP Yield Curve")

    curveFitMethod = CurveFitNelsonSiegel()
    fittedCurve3 = BondYieldCurve(settlement, bonds, ylds, curveFitMethod)
#    fittedCurve3.display("GBP Yield Curve")

    curveFitMethod = CurveFitNelsonSiegelSvensson()
    fittedCurve4 = BondYieldCurve(settlement, bonds, ylds, curveFitMethod)
#    fittedCurve4.display("GBP Yield Curve")

    curveFitMethod = CurveFitBSpline()
    fittedCurve5 = BondYieldCurve(settlement, bonds, ylds, curveFitMethod)
#    fittedCurve5.display("GBP Yield Curve")

###############################################################################

    testCases.header("PARAMETER", "VALUE")
    testCases.print("beta1", fittedCurve3._curveFit._beta1)
    testCases.print("beta2", fittedCurve3._curveFit._beta2)
    testCases.print("beta3", fittedCurve3._curveFit._beta3)
    testCases.print("tau", fittedCurve3._curveFit._tau)

    testCases.header("PARAMETER", "VALUE")
    testCases.print("beta1", fittedCurve4._curveFit._beta1)
    testCases.print("beta2", fittedCurve4._curveFit._beta2)
    testCases.print("beta3", fittedCurve4._curveFit._beta3)
    testCases.print("beta4", fittedCurve4._curveFit._beta4)
    testCases.print("tau1", fittedCurve4._curveFit._tau1)
    testCases.print("tau2", fittedCurve4._curveFit._tau2)

###############################################################################

    maturity_date = Date(19, 9, 2030)
    interpolatedYield = fittedCurve5.interpolatedYield(maturity_date)
    testCases.print(maturity_date, interpolatedYield)

###############################################################################


test_BondYieldCurve()
testCases.compareTestCases()
