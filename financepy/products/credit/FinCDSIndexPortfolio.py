##############################################################################
# Copyright (C) 2018, 2019, 2020 Dominic O'Kane
##############################################################################


from math import pow

from ...utils.Calendar import FinCalendarTypes
from ...utils.Calendar import FinBusDayAdjustTypes, FinDateGenRuleTypes
from ...utils.DayCount import FinDayCountTypes
from ...utils.Frequency import FinFrequencyTypes
from ...utils.FinError import FinError
from ...products.credit.FinCDS import FinCDS
from ...products.credit.FinCDSCurve import FinCDSCurve
from ...utils.FinHelperFunctions import checkArgumentTypes
from ...utils.FinHelperFunctions import labelToString

###############################################################################
# TODO: Move index spread details into class and then pass in issuer curves
#       to the function when doing the adjustment
###############################################################################


class FinCDSIndexPortfolio():
    """ This class manages the calculations associated with an equally weighted
    portfolio of CDS contracts with the same maturity date. """

    def __init__(self,
                 freq_type: FinFrequencyTypes = FinFrequencyTypes.QUARTERLY,
                 day_count_type: FinDayCountTypes = FinDayCountTypes.ACT_360,
                 calendar_type: FinCalendarTypes = FinCalendarTypes.WEEKEND,
                 bus_day_adjust_type: FinBusDayAdjustTypes = FinBusDayAdjustTypes.FOLLOWING,
                 date_gen_rule_type: FinDateGenRuleTypes = FinDateGenRuleTypes.BACKWARD):
        """ Create FinCDSIndexPortfolio object. Note that all of the inputs
        have a default value which reflects the CDS market standard. """

        checkArgumentTypes(self.__init__, locals())

        self._day_count_type = day_count_type
        self._date_gen_rule_type = date_gen_rule_type
        self._calendar_type = calendar_type
        self._freq_type = freq_type
        self._bus_day_adjust_type = bus_day_adjust_type

###############################################################################

    def intrinsicRPV01(self,
                       valuation_date,
                       step_in_date,
                       maturity_date,
                       issuer_curves):
        """ Calculation of the risky PV01 of the CDS porfolio by taking the
        average of the risky PV01s of each contract. """

        numCredits = len(issuer_curves)

        cdsContract = FinCDS(step_in_date,
                             maturity_date,
                             0.0)

        intrinsicRPV01 = 0.0

        for m in range(0, numCredits):

            retValue = cdsContract.riskyPV01(valuation_date,
                                             issuer_curves[m])

            cleanRPV01 = retValue['clean_rpv01']

            intrinsicRPV01 += cleanRPV01

        intrinsicRPV01 /= numCredits
        return(intrinsicRPV01)

###############################################################################

    def intrinsicProtectionLegPV(self,
                                 valuation_date,
                                 step_in_date,
                                 maturity_date,
                                 issuer_curves):
        """ Calculation of intrinsic protection leg value of the CDS porfolio
        by taking the average sum the protection legs of each contract. """

        numCredits = len(issuer_curves)

        intrinsicProtPV = 0.0

        # All contracts have same flows so only need one object
        cdsContract = FinCDS(step_in_date,
                             maturity_date,
                             0.0,
                             1.0)

        for m in range(0, numCredits):

            protectionPV = cdsContract.protectionLegPV(valuation_date,
                                                       issuer_curves[m])

            intrinsicProtPV += protectionPV

        intrinsicProtPV /= numCredits
        return intrinsicProtPV

###############################################################################

    def intrinsicSpread(self,
                        valuation_date,
                        step_in_date,
                        maturity_date,
                        issuer_curves):
        """ Calculation of the intrinsic spread of the CDS portfolio as the one
        which would make the value of the protection legs equal to the value of
        the premium legs if all premium legs paid the same spread. """

        intrinsicProtPV = self.intrinsicProtectionLegPV(valuation_date,
                                                        step_in_date,
                                                        maturity_date,
                                                        issuer_curves)

        intrinsicRPV01 = self.intrinsicRPV01(valuation_date,
                                             step_in_date,
                                             maturity_date,
                                             issuer_curves)

        intrinsicSpread = intrinsicProtPV / intrinsicRPV01

        return(intrinsicSpread)

###############################################################################

    def averageSpread(self,
                      valuation_date,
                      step_in_date,
                      maturity_date,
                      issuer_curves):
        """ Calculates the average par CDS spread of the CDS portfolio. """

        numCredits = len(issuer_curves)

        cdsContract = FinCDS(step_in_date,
                             maturity_date,
                             0.0)

        averageSpread = 0.0

        for m in range(0, numCredits):
            spread = cdsContract.parSpread(valuation_date, issuer_curves[m])
            averageSpread += spread

        averageSpread /= numCredits
        return averageSpread

###############################################################################

    def totalSpread(self,
                    valuation_date,
                    step_in_date,
                    maturity_date,
                    issuer_curves):
        """ Calculates the total CDS spread of the CDS portfolio by summing
        over all of the issuers and adding the spread with no weights. """

        numCredits = len(issuer_curves)

        cdsContract = FinCDS(step_in_date,
                             maturity_date,
                             0.0)

        totalSpread = 0.0

        for m in range(0, numCredits):
            spread = cdsContract.parSpread(valuation_date, issuer_curves[m])
            totalSpread += spread

        return totalSpread

###############################################################################

    def minSpread(self,
                  valuation_date,
                  step_in_date,
                  maturity_date,
                  issuer_curves):
        """ Calculates the minimum par CDS spread across all of the issuers in
        the CDS portfolio. """

        numCredits = len(issuer_curves)

        if numCredits < 1:
            raise FinError("Number of credits in index must be > 1 and not" + str(numCredits))

        cdsContract = FinCDS(step_in_date,
                             maturity_date,
                             0.0)

        minSpread = cdsContract.parSpread(valuation_date, issuer_curves[0])

        for m in range(1, numCredits):
            spread = cdsContract.parSpread(valuation_date, issuer_curves[m])
            if spread < minSpread:
                minSpread = spread

        return minSpread

###############################################################################

    def maxSpread(self,
                  valuation_date,
                  step_in_date,
                  maturity_date,
                  issuer_curves):
        """ Calculates the maximum par CDS spread across all of the issuers in
        the CDS portfolio. """

        numCredits = len(issuer_curves)

        if numCredits < 1:
            raise FinError("Number of credits in index must be > 1 and not " + str(numCredits))

        cdsContract = FinCDS(step_in_date,
                             maturity_date,
                             0.0)

        maxSpread = cdsContract.parSpread(valuation_date, issuer_curves[0])

        for m in range(1, numCredits):
            spread = cdsContract.parSpread(valuation_date, issuer_curves[m])
            if spread > maxSpread:
                maxSpread = spread

        return maxSpread

###############################################################################

    def spreadAdjustIntrinsic(self,
                              valuation_date,
                              issuer_curves,
                              indexCoupons,
                              indexUpfronts,
                              indexMaturityDates,
                              indexRecoveryRate,
                              tolerance=1e-6):
        """ Adjust individual CDS curves to reprice CDS index prices.
        This approach uses an iterative scheme but is slow as it has to use a
        CDS curve bootstrap required when each trial spread adjustment is made
        """

        numCredits = len(issuer_curves)

        if numCredits < 1:
            raise FinError("Number of credits in index must be > 1 and not " + str(numCredits))

        libor_curve = issuer_curves[0]._libor_curve
        numIndexMaturityPoints = len(indexCoupons)

        cdsMaturityDates = []
        for cds in issuer_curves[0]._cds_contracts:
            cdsDates = cds._maturity_date
            cdsMaturityDates.append(cdsDates)

        numCDSMaturityPoints = len(cdsMaturityDates)

        for issuer_curve in issuer_curves:
            n = len(issuer_curve._cds_contracts)
            if n != len(cdsMaturityDates):
                raise FinError(
                    "All issuer curves must be built from same cds maturities")

        cdsSpreadMultipliers = [1.0] * numCDSMaturityPoints

#        spreadDifference = [0.0] * numCDSMaturityPoints

        adjustedCDSSpreads = [0.0] * numCDSMaturityPoints

        #######################################################################
        # Set up CDS contracts used to build curve
        #######################################################################

        curveCDSContracts = []

        for j in range(0, numCDSMaturityPoints):

            cdsCoupon = 1.0

            cdsContract = FinCDS(valuation_date,
                                 cdsMaturityDates[j],
                                 cdsCoupon)

            curveCDSContracts.append(cdsContract)

        #######################################################################

        # We calibrate the individual CDS curves to fit each index maturity
        # point
        for iMaturity in range(0, numIndexMaturityPoints):

            alpha = 0.0
            numIterations = 0

            while abs(alpha - 1.0) > tolerance:

                numIterations += 1

                if numIterations > 20:
                    raise FinError(
                        "Num iterations > 20. Increase limit or reduce tolerance or check inputs.")

                sumRPV01 = 0.0
                sumProt = 0.0

                # This is for the specific index maturity date
                indexMaturityDate = indexMaturityDates[iMaturity]
                cdsIndex = FinCDS(valuation_date, indexMaturityDate, 0.0, 1.0)

                for iCredit in range(0, numCredits):

                    cds_contracts = issuer_curves[iCredit]._cds_contracts
                    recovery_rate = issuer_curves[iCredit]._recovery_rate
                    adjustedCDSContracts = []

                    for j in range(0, numCDSMaturityPoints):

                        cdsSpread = cds_contracts[j]._running_coupon
                        adjustedCDSSpreads[j] = cdsSpread * \
                            cdsSpreadMultipliers[j]
                        curveCDSContracts[j]._running_coupon = adjustedCDSSpreads[j]

                    adjustedIssuerCurve = FinCDSCurve(valuation_date,
                                                      curveCDSContracts,
                                                      libor_curve,
                                                      recovery_rate)

                    indexProtectionPV = cdsIndex.protectionLegPV(valuation_date,
                                                                 adjustedIssuerCurve,
                                                                 indexRecoveryRate)

                    cleanRPV01 = cdsIndex.riskyPV01(valuation_date,
                                                    adjustedIssuerCurve)['clean_rpv01']

                    sumRPV01 += cleanRPV01
                    sumProt += indexProtectionPV

                sumRPV01 /= numCredits
                sumProt /= numCredits

                sumPrem = sumRPV01 * indexCoupons[iMaturity]

                numerator = indexUpfronts[iMaturity] + sumPrem
                denominator = sumProt

                alpha = numerator / denominator
                cdsSpreadMultipliers[iMaturity] *= alpha

        # use spread multipliers to build and store adjusted curves
        adjustedIssuerCurves = []

        for iCredit in range(0, numCredits):

            recovery_rate = issuer_curves[iCredit]._recovery_rate

            adjustedCDSContracts = []
            adjustedSpreads = []

            for j in range(0, numCDSMaturityPoints):

                unadjustedSpread = issuer_curves[iCredit]._cds_contracts[j]._running_coupon

                adjustedSpread = unadjustedSpread * cdsSpreadMultipliers[j]

                adjustedcdsContract = FinCDS(valuation_date,
                                             cdsMaturityDates[j],
                                             adjustedSpread)

                adjustedCDSContracts.append(adjustedcdsContract)
                adjustedSpreads.append(adjustedSpread)

                adjustedIssuerCurve = FinCDSCurve(valuation_date,
                                                  adjustedCDSContracts,
                                                  libor_curve,
                                                  recovery_rate)

            adjustedIssuerCurves.append(adjustedIssuerCurve)

        return adjustedIssuerCurves

###############################################################################

    def hazardRateAdjustIntrinsic(self,
                                  valuation_date,
                                  issuer_curves,
                                  indexCoupons,
                                  indexUpfronts,
                                  indexMaturityDates,
                                  indexRecoveryRate,
                                  tolerance=1e-6,
                                  maxIterations=100):
        """ Adjust individual CDS curves to reprice CDS index prices.
        This approach adjusts the hazard rates and so avoids the slowish
        CDS curve bootstrap required when a spread adjustment is made."""
        numCredits = len(issuer_curves)

        if numCredits < 1:
            raise FinError("Number of credits must be greater than 1")

        libor_curve = issuer_curves[0]._libor_curve
        numIndexMaturityPoints = len(indexCoupons)
#        hazardRateMultipliers = [1.0] * numIndexMaturityPoints
        adjustedIssuerCurves = []

        # making a copy of the issuer curves
        for issuer_curve in issuer_curves:

            adjustedIssuerCurve = FinCDSCurve(valuation_date,
                                              [],
                                              libor_curve)

            adjustedIssuerCurve._times = issuer_curve._times.copy()
            adjustedIssuerCurve._values = issuer_curve._values.copy()
            adjustedIssuerCurves.append(adjustedIssuerCurve)

        # We solve for each maturity point
        for iMaturity in range(0, numIndexMaturityPoints):

            alpha = 1.0
            ratio = 1.0 + 2.0 * tolerance
            numIterations = 0

            while abs(ratio - 1.0) > tolerance:

                numIterations += 1

                if numIterations == maxIterations:
                    raise FinError("Max Iterations exceeded")

                sumRPV01 = 0.0
                sumProt = 0.0

                for iCredit in range(0, numCredits):

                    q1 = adjustedIssuerCurves[iCredit]._values[iMaturity]
                    q2 = adjustedIssuerCurves[iCredit]._values[iMaturity + 1]
                    q12 = q2 / q1
                    q12NEW = pow(q12, ratio)
                    q2NEW = q1 * q12NEW

                    adjustedIssuerCurves[iCredit]._values[iMaturity + 1] = q2NEW

                    indexMaturityDate = indexMaturityDates[iMaturity]

                    # the CDS spreads we extract here should be the index
                    # maturity dates
                    cdsIndex = FinCDS(valuation_date, indexMaturityDate, 0, 1.0)

                    indexProtPV = cdsIndex.protectionLegPV(valuation_date,
                                                           adjustedIssuerCurves[iCredit],
                                                           indexRecoveryRate)

                    rpv01Ret = cdsIndex.riskyPV01(
                        valuation_date, adjustedIssuerCurves[iCredit])

                    cleanRPV01 = rpv01Ret['clean_rpv01']

                    sumRPV01 += cleanRPV01
                    sumProt += indexProtPV

                sumRPV01 /= numCredits
                sumProt /= numCredits
                sumPrem = sumRPV01 * indexCoupons[iMaturity]

                numerator = indexUpfronts[iMaturity] + sumPrem
                denominator = sumProt

                ratio = numerator / denominator
                alpha *= ratio

        return adjustedIssuerCurves

###############################################################################

    def __repr__(self):

        s = labelToString("OBJECT TYPE", type(self).__name__)
        s += labelToString("FREQUENCY", self._freq_type)
        s += labelToString("DAYCOUNT", self._day_count_type)
        s += labelToString("CALENDAR", self._calendar_type)
        s += labelToString("BUSDAYRULE", self._bus_day_adjust_type)
        s += labelToString("DATEGENRULE", self._date_gen_rule_type)
        return s

###############################################################################

    def _print(self):
        """ Simple print function for backward compatibility. """
        print(self)

###############################################################################
