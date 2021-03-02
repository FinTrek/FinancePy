###############################################################################
# Copyright (C) 2018, 2019, 2020 Dominic O'Kane
###############################################################################

import sys
sys.path.append("..")

from financepy.products.equity.FinEquityOneTouchOption import FinEquityOneTouchOption
from financepy.products.equity.FinEquityOneTouchOption import FinTouchOptionPayoffTypes
from financepy.market.curves.FinDiscountCurveFlat import FinDiscountCurveFlat
from financepy.models.FinModelBlackScholes import FinModelBlackScholes
from financepy.utils.Date import Date

from FinTestCases import FinTestCases, globalTestCaseMode
testCases = FinTestCases(__file__, globalTestCaseMode)

###############################################################################


def test_FinFXOneTouchOption():
    # Examples Haug Page 180 Table 4-22
    # Agreement not exact at t is not exactly 0.50

    valuation_date = Date(1, 1, 2016)
    expiry_date = Date(2, 7, 2016)
    volatility = 0.20
    barrierLevel = 1.0  # H
    model = FinModelBlackScholes(volatility)

    domesticRate = 0.10
    foreignRate = 0.03

    numPaths = 20000
    num_steps_per_year = 252

    domCurve = FinDiscountCurveFlat(valuation_date, domesticRate)
    forCurve = FinDiscountCurveFlat(valuation_date, foreignRate)

    spotFXRate = 1.050
    paymentSize = 1.5

    testCases.header("================================= CASH ONLY")

    downTypes = [FinTouchOptionPayoffTypes.DOWN_AND_IN_CASH_AT_HIT,
                 FinTouchOptionPayoffTypes.DOWN_AND_IN_CASH_AT_EXPIRY,
                 FinTouchOptionPayoffTypes.DOWN_AND_OUT_CASH_OR_NOTHING]

    testCases.header("TYPE", "VALUE", "VALUE_MC")

    for downType in downTypes:

        option = FinEquityOneTouchOption(expiry_date,
                                         downType,
                                         barrierLevel,
                                         paymentSize)

        v = option.value(valuation_date,
                         spotFXRate,
                         domCurve,
                         forCurve,
                         model)

        v_mc = option.valueMC(valuation_date,
                              spotFXRate,
                              domCurve,
                              forCurve,
                              model,
                              num_steps_per_year,
                              numPaths)

        testCases.print("%60s " % downType,
                        "%9.5f" % v,
                        "%9.5f" % v_mc)

    spotFXRate = 0.950
    paymentSize = 1.5

    upTypes = [FinTouchOptionPayoffTypes.UP_AND_IN_CASH_AT_HIT,
               FinTouchOptionPayoffTypes.UP_AND_IN_CASH_AT_EXPIRY,
               FinTouchOptionPayoffTypes.UP_AND_OUT_CASH_OR_NOTHING]

    testCases.header("TYPE", "VALUE", "VALUE_MC")

    for upType in upTypes:

        option = FinEquityOneTouchOption(expiry_date,
                                         upType,
                                         barrierLevel,
                                         paymentSize)

        v = option.value(valuation_date,
                         spotFXRate,
                         domCurve,
                         forCurve,
                         model)

        v_mc = option.valueMC(valuation_date,
                              spotFXRate,
                              domCurve,
                              forCurve,
                              model,
                              num_steps_per_year,
                              numPaths)

        testCases.print("%60s " % upType,
                        "%9.5f" % v,
                        "%9.5f" % v_mc)

    ###########################################################################

    spotFXRate = 1.050

    testCases.banner("================= ASSET ONLY")

    downTypes = [FinTouchOptionPayoffTypes.DOWN_AND_IN_ASSET_AT_HIT,
                 FinTouchOptionPayoffTypes.DOWN_AND_IN_ASSET_AT_EXPIRY,
                 FinTouchOptionPayoffTypes.DOWN_AND_OUT_ASSET_OR_NOTHING]

    testCases.header("TYPE", "VALUE", "VALUE_MC")
    for downType in downTypes:

        option = FinEquityOneTouchOption(expiry_date,
                                         downType,
                                         barrierLevel)

        v = option.value(valuation_date,
                         spotFXRate,
                         domCurve,
                         forCurve,
                         model)

        v_mc = option.valueMC(valuation_date,
                              spotFXRate,
                              domCurve,
                              forCurve,
                              model,
                              num_steps_per_year,
                              numPaths)

        testCases.print("%60s " % downType,
                        "%9.5f" % v,
                        "%9.5f" % v_mc)

    spotFXRate = 0.950

    upTypes = [FinTouchOptionPayoffTypes.UP_AND_IN_ASSET_AT_HIT,
               FinTouchOptionPayoffTypes.UP_AND_IN_ASSET_AT_EXPIRY,
               FinTouchOptionPayoffTypes.UP_AND_OUT_ASSET_OR_NOTHING]

    for upType in upTypes:

        option = FinEquityOneTouchOption(expiry_date,
                                         upType,
                                         barrierLevel)

        v = option.value(valuation_date,
                         spotFXRate,
                         domCurve,
                         forCurve,
                         model)

        v_mc = option.valueMC(valuation_date,
                              spotFXRate,
                              domCurve,
                              forCurve,
                              model,
                              num_steps_per_year,
                              numPaths)

        testCases.print("%60s " % upType,
                        "%9.5f" % v,
                        "%9.5f" % v_mc)

###############################################################################


test_FinFXOneTouchOption()
testCases.compareTestCases()
