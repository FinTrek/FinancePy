##############################################################################
# Copyright (C) 2018, 2019, 2020 Dominic O'Kane
##############################################################################


from ...utils.FinError import FinError
from ...utils.Frequency import Frequency, FinFrequencyTypes
from ...utils.Calendar import FinCalendarTypes
from ...utils.Schedule import Schedule
from ...utils.Calendar import FinBusDayAdjustTypes
from ...utils.Calendar import FinDateGenRuleTypes
from ...utils.DayCount import FinDayCountTypes
from ...utils.Date import Date
from ...utils.FinHelperFunctions import labelToString, checkArgumentTypes

###############################################################################

from enum import Enum


class FinBondMortgageTypes(Enum):
    REPAYMENT = 1
    INTEREST_ONLY = 2

###############################################################################


class FinBondMortgage(object):
    """ A mortgage is a vector of dates and flows generated in order to repay
    a fixed amount given a known interest rate. Payments are all the same
    amount but with a varying mixture of interest and repayment of principal.
    """

    def __init__(self,
                 start_date: Date,
                 end_date: Date,
                 principal: float,
                 freq_type: FinFrequencyTypes = FinFrequencyTypes.MONTHLY,
                 calendar_type: FinCalendarTypes = FinCalendarTypes.WEEKEND,
                 bus_day_adjust_type: FinBusDayAdjustTypes = FinBusDayAdjustTypes.FOLLOWING,
                 date_gen_rule_type: FinDateGenRuleTypes = FinDateGenRuleTypes.BACKWARD,
                 dayCountConventionType: FinDayCountTypes = FinDayCountTypes.ACT_360):
        """ Create the mortgage using start and end dates and principal. """

        checkArgumentTypes(self.__init__, locals())

        if start_date > end_date:
            raise FinError("Start Date after End Date")

        self._start_date = start_date
        self._end_date = end_date
        self._principal = principal
        self._freq_type = freq_type
        self._calendar_type = calendar_type
        self._bus_day_adjust_type = bus_day_adjust_type
        self._date_gen_rule_type = date_gen_rule_type
        self._dayCountConventionType = dayCountConventionType

        self._schedule = Schedule(start_date,
                                  end_date,
                                  self._freq_type,
                                  self._calendar_type,
                                  self._bus_day_adjust_type,
                                  self._date_gen_rule_type)

###############################################################################

    def repaymentAmount(self,
                        zeroRate: float):
        """ Determine monthly repayment amount based on current zero rate. """

        frequency = Frequency(self._freq_type)

        numFlows = len(self._schedule._adjustedDates)
        p = (1.0 + zeroRate/frequency) ** (numFlows-1)
        m = zeroRate * p / (p - 1.0) / frequency
        m = m * self._principal
        return m

###############################################################################

    def generateFlows(self,
                      zeroRate: float,
                      mortgageType: FinBondMortgageTypes):
        """ Generate the bond flow amounts. """

        self._mortgageType = mortgageType
        self._interestFlows = [0]
        self._principalFlows = [0]
        self._principalRemaining = [self._principal]
        self._totalFlows = [0]

        numFlows = len(self._schedule._adjustedDates)
        principal = self._principal
        frequency = Frequency(self._freq_type)

        if mortgageType == FinBondMortgageTypes.REPAYMENT:
            monthlyFlow = self.repaymentAmount(zeroRate)
        elif mortgageType == FinBondMortgageTypes.INTEREST_ONLY:
            monthlyFlow = zeroRate * self._principal / frequency
        else:
            raise FinError("Unknown Mortgage type.")

        for i in range(1, numFlows):
            interestFlow = principal * zeroRate / frequency
            principalFlow = monthlyFlow - interestFlow
            principal = principal - principalFlow
            self._interestFlows.append(interestFlow)
            self._principalFlows.append(principalFlow)
            self._principalRemaining.append(principal)
            self._totalFlows.append(monthlyFlow)

###############################################################################

    def printLeg(self):
        print("START DATE:", self._start_date)
        print("MATURITY DATE:", self._end_date)
        print("MORTGAGE TYPE:", self._mortgageType)
        print("FREQUENCY:", self._freq_type)
        print("CALENDAR:", self._calendar_type)
        print("BUSDAYRULE:", self._bus_day_adjust_type)
        print("DATEGENRULE:", self._date_gen_rule_type)

        numFlows = len(self._schedule._adjustedDates)

        print("%15s %12s %12s %12s %12s" %
              ("PAYMENT DATE", "INTEREST", "PRINCIPAL",
               "OUTSTANDING", "TOTAL"))

        print("")
        for i in range(0, numFlows):
            print("%15s %12.2f %12.2f %12.2f %12.2f" %
                  (self._schedule._adjustedDates[i],
                   self._interestFlows[i],
                   self._principalFlows[i],
                   self._principalRemaining[i],
                   self._totalFlows[i]))

###############################################################################

    def __repr__(self):
        s = labelToString("OBJECT TYPE", type(self).__name__)
        s += labelToString("START DATE", self._start_date)
        s += labelToString("MATURITY DATE", self._end_date)
        s += labelToString("MORTGAGE TYPE", self._mortgageType)
        s += labelToString("FREQUENCY", self._freq_type)
        s += labelToString("CALENDAR", self._calendar_type)
        s += labelToString("BUSDAYRULE", self._bus_day_adjust_type)
        s += labelToString("DATEGENRULE", self._date_gen_rule_type)
        return s

###############################################################################

    def _print(self):
        """ Simple print function for backward compatibility. """
        print(self)

###############################################################################
