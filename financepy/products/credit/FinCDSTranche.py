##############################################################################
# Copyright (C) 2018, 2019, 2020 Dominic O'Kane
##############################################################################

# TODO: Add __repr__ method

import numpy as np
from math import sqrt


from ...models.FinModelGaussianCopula1F import trSurvProbGaussian
from ...models.FinModelGaussianCopula1F import trSurvProbAdjBinomial
from ...models.FinModelGaussianCopula1F import trSurvProbRecursion
from ...models.FinModelGaussianCopulaLHP import trSurvProbLHP

from ...utils.DayCount import FinDayCountTypes
from ...utils.Frequency import FinFrequencyTypes
from ...utils.Calendar import FinCalendarTypes
from ...utils.Calendar import FinBusDayAdjustTypes, FinDateGenRuleTypes

from ...products.credit.FinCDS import FinCDS
from ...products.credit.FinCDSCurve import FinCDSCurve

from ...utils.FinGlobalVariables import gDaysInYear
from ...utils.Math import ONE_MILLION
from ...market.curves.FinInterpolator import FinInterpTypes, interpolate
from ...utils.FinError import FinError

from ...utils.FinHelperFunctions import checkArgumentTypes
from ...utils.Date import Date

###############################################################################

from enum import Enum


class FinLossDistributionBuilder(Enum):
    RECURSION = 1
    ADJUSTED_BINOMIAL = 2
    GAUSSIAN = 3
    LHP = 4

###############################################################################


class FinCDSTranche(object):

    def __init__(self,
                 step_in_date: Date,
                 maturity_date: Date,
                 k1: float,
                 k2: float,
                 notional: float = ONE_MILLION,
                 running_coupon: float = 0.0,
                 long_protection: bool = True,
                 freq_type: FinFrequencyTypes = FinFrequencyTypes.QUARTERLY,
                 day_count_type: FinDayCountTypes = FinDayCountTypes.ACT_360,
                 calendar_type: FinCalendarTypes = FinCalendarTypes.WEEKEND,
                 bus_day_adjust_type: FinBusDayAdjustTypes = FinBusDayAdjustTypes.FOLLOWING,
                 date_gen_rule_type: FinDateGenRuleTypes = FinDateGenRuleTypes.BACKWARD):

        checkArgumentTypes(self.__init__, locals())

        if k1 >= k2:
            raise FinError("K1 must be less than K2")

        self._k1 = k1
        self._k2 = k2

        self._step_in_date = step_in_date
        self._maturity_date = maturity_date
        self._notional = notional
        self._running_coupon = running_coupon
        self._long_protection = long_protection
        self._day_count_type = day_count_type
        self._date_gen_rule_type = date_gen_rule_type
        self._calendar_type = calendar_type
        self._freq_type = freq_type
        self._bus_day_adjust_type = bus_day_adjust_type

        notional = 1.0

        self._cdsContract = FinCDS(self._step_in_date,
                                   self._maturity_date,
                                   self._running_coupon,
                                   notional,
                                   self._long_protection,
                                   self._freq_type,
                                   self._day_count_type,
                                   self._calendar_type,
                                   self._bus_day_adjust_type,
                                   self._date_gen_rule_type)

###############################################################################

    def valueBC(self,
                valuation_date,
                issuer_curves,
                upfront,
                running_coupon,
                corr1,
                corr2,
                num_points=50,
                model=FinLossDistributionBuilder.RECURSION):

        numCredits = len(issuer_curves)
        k1 = self._k1
        k2 = self._k2
        tmat = (self._maturity_date - valuation_date) / gDaysInYear

        if tmat < 0.0:
            raise FinError("Value date is after maturity date")

        if abs(k1 - k2) < 0.00000001:
            output = np.zeros(4)
            output[0] = 0.0
            output[1] = 0.0
            output[2] = 0.0
            output[3] = 0.0
            return output

        if k1 > k2:
            raise FinError("K1 > K2")

        kappa = k2 / (k2 - k1)

        recovery_rates = np.zeros(numCredits)

        payment_dates = self._cdsContract._adjustedDates
        numTimes = len(payment_dates)

        beta1 = sqrt(corr1)
        beta2 = sqrt(corr2)
        betaVector1 = np.zeros(numCredits)
        for bb in range(0, numCredits):
            betaVector1[bb] = beta1

        betaVector2 = np.zeros(numCredits)
        for bb in range(0, numCredits):
            betaVector2[bb] = beta2

        qVector = np.zeros(numCredits)
        qt1 = np.zeros(numTimes)
        qt2 = np.zeros(numTimes)
        trancheTimes = np.zeros(numTimes)
        trancheSurvivalCurve = np.zeros(numTimes)

        trancheTimes[0] = 0
        trancheSurvivalCurve[0] = 1.0
        qt1[0] = 1.0
        qt2[0] = 1.0

        for i in range(1, numTimes):

            t = (payment_dates[i] - valuation_date) / gDaysInYear

            for j in range(0, numCredits):

                issuer_curve = issuer_curves[j]
                vTimes = issuer_curve._times
                qRow = issuer_curve._values
                recovery_rates[j] = issuer_curve._recovery_rate
                qVector[j] = interpolate(
                    t, vTimes, qRow, FinInterpTypes.FLAT_FWD_RATES.value)

            if model == FinLossDistributionBuilder.RECURSION:
                qt1[i] = trSurvProbRecursion(
                    0.0, k1, numCredits, qVector, recovery_rates,
                    betaVector1, num_points)
                qt2[i] = trSurvProbRecursion(
                    0.0, k2, numCredits, qVector, recovery_rates,
                    betaVector2, num_points)
            elif model == FinLossDistributionBuilder.ADJUSTED_BINOMIAL:
                qt1[i] = trSurvProbAdjBinomial(
                    0.0, k1, numCredits, qVector, recovery_rates,
                    betaVector1, num_points)
                qt2[i] = trSurvProbAdjBinomial(
                    0.0, k2, numCredits, qVector, recovery_rates,
                    betaVector2, num_points)
            elif model == FinLossDistributionBuilder.GAUSSIAN:
                qt1[i] = trSurvProbGaussian(
                    0.0,
                    k1,
                    numCredits,
                    qVector,
                    recovery_rates,
                    betaVector1,
                    num_points)
                qt2[i] = trSurvProbGaussian(
                    0.0,
                    k2,
                    numCredits,
                    qVector,
                    recovery_rates,
                    betaVector2,
                    num_points)
            elif model == FinLossDistributionBuilder.LHP:
                qt1[i] = trSurvProbLHP(
                    0.0, k1, numCredits, qVector, recovery_rates, beta1)
                qt2[i] = trSurvProbLHP(
                    0.0, k2, numCredits, qVector, recovery_rates, beta2)
            else:
                raise FinError(
                    "Unknown model type only full and AdjBinomial allowed")

            if qt1[i] > qt1[i - 1]:
                raise FinError(
                    "Tranche K1 survival probabilities not decreasing.")

            if qt2[i] > qt2[i - 1]:
                raise FinError(
                    "Tranche K2 survival probabilities not decreasing.")

            trancheSurvivalCurve[i] = kappa * qt2[i] + (1.0 - kappa) * qt1[i]
            trancheTimes[i] = t

        curveRecovery = 0.0  # For tranches only
        libor_curve = issuer_curves[0]._libor_curve
        trancheCurve = FinCDSCurve(
            valuation_date, [], libor_curve, curveRecovery)
        trancheCurve._times = trancheTimes
        trancheCurve._values = trancheSurvivalCurve

        protLegPV = self._cdsContract.protectionLegPV(
            valuation_date, trancheCurve, curveRecovery)
        riskyPV01 = self._cdsContract.riskyPV01(valuation_date, trancheCurve)['clean_rpv01']

        mtm = self._notional * (protLegPV - upfront - riskyPV01 * running_coupon)

        if not self._long_protection:
            mtm *= -1.0

        trancheOutput = np.zeros(4)
        trancheOutput[0] = mtm
        trancheOutput[1] = riskyPV01 * self._notional * running_coupon
        trancheOutput[2] = protLegPV * self._notional
        trancheOutput[3] = protLegPV / riskyPV01

        return trancheOutput

###############################################################################
