##############################################################################
# Copyright (C) 2018, 2019, 2020 Dominic O'Kane
##############################################################################


import numpy as np
import matplotlib.pyplot as plt

from ...utils.FinError import FinError
from ...utils.Date import Date
from ...utils.FinGlobalVariables import gDaysInYear
from ...utils.Math import scale
from ...utils.FinHelperFunctions import labelToString

from .FinBondYieldCurveModel import FinCurveFitPolynomial
from .FinBondYieldCurveModel import FinCurveFitNelsonSiegel
from .FinBondYieldCurveModel import FinCurveFitNelsonSiegelSvensson
from .FinBondYieldCurveModel import FinCurveFitBSpline

from scipy.optimize import curve_fit
from scipy.interpolate import splrep

###############################################################################
# TO DO: CONSTRAIN TAU'S IN NELSON-SIEGEL
###############################################################################


class FinBondYieldCurve():
    """ Class to do fitting of the yield curve and to enable interpolation of
    yields. Because yields assume a flat term structure for each bond, this
    class does not allow discounting to be done and so does not inherit from
    FinDiscountCurve. It should only be used for visualisation and simple
    interpolation but not for full term-structure-consistent pricing. """

    def __init__(self,
                 settlement_date: Date,
                 bonds: list,
                 ylds: (np.ndarray, list),
                 curveFit):
        """ Fit the curve to a set of bond yields using the type of curve
        specified. Bounds can be provided if you wish to enforce lower and
        upper limits on the respective model parameters. """

        self._settlement_date = settlement_date
        self._bonds = bonds
        self._ylds = np.array(ylds)
        self._curveFit = curveFit

        fitType = type(self._curveFit)
        fit = self._curveFit

        yearsToMaturities = []
        for bond in bonds:
            maturityYears = (bond._maturity_date-settlement_date)/gDaysInYear
            yearsToMaturities.append(maturityYears)
        self._yearsToMaturity = np.array(yearsToMaturities)

        if fitType is FinCurveFitPolynomial:

            d = fit._power
            coeffs = np.polyfit(self._yearsToMaturity, self._ylds, deg=d)
            fit._coeffs = coeffs

        elif fitType is FinCurveFitNelsonSiegel:

            xdata = self._yearsToMaturity
            ydata = self._ylds

            popt, pcov = curve_fit(self._curveFit._interpolatedYield,
                                   xdata, ydata, bounds=fit._bounds)

            fit._beta1 = popt[0]
            fit._beta2 = popt[1]
            fit._beta3 = popt[2]
            fit._tau = popt[3]

        elif fitType is FinCurveFitNelsonSiegelSvensson:

            xdata = self._yearsToMaturity
            ydata = self._ylds

            popt, pcov = curve_fit(self._curveFit._interpolatedYield,
                                   xdata, ydata, bounds=fit._bounds)

            fit._beta1 = popt[0]
            fit._beta2 = popt[1]
            fit._beta3 = popt[2]
            fit._beta4 = popt[3]
            fit._tau1 = popt[4]
            fit._tau2 = popt[5]

        elif fitType is FinCurveFitBSpline:

            xdata = self._yearsToMaturity
            ydata = self._ylds

            """ Cubic splines as k=3 """
            spline = splrep(xdata, ydata, k=fit._power, t=fit._knots)
            fit._spline = spline

        else:
            raise FinError("Unrecognised curve fit type.")

###############################################################################

    def interpolatedYield(self,
                          maturity_date: Date):

        if type(maturity_date) is Date:
            t = (maturity_date - self._settlement_date) / gDaysInYear
        elif type(maturity_date) is list:
            t = maturity_date
        elif type(maturity_date) is np.ndarray:
            t = maturity_date
        elif type(maturity_date) is float or type(maturity_date) is np.float64:
            t = maturity_date
        else:
            raise FinError("Unknown date type.")

        fit = self._curveFit

        if type(fit) == FinCurveFitPolynomial:
            yld = fit._interpolatedYield(t)
        elif type(fit) == FinCurveFitNelsonSiegel:
            yld = fit._interpolatedYield(t,
                                         fit._beta1,
                                         fit._beta2,
                                         fit._beta3,
                                         fit._tau)

        elif type(fit) == FinCurveFitNelsonSiegelSvensson:
            yld = fit._interpolatedYield(t,
                                         fit._beta1,
                                         fit._beta2,
                                         fit._beta3,
                                         fit._beta4,
                                         fit._tau1,
                                         fit._tau2)

        elif type(fit) == FinCurveFitBSpline:
            yld = fit._interpolatedYield(t)

        return yld

###############################################################################

    def plot(self,
             title):
        """ Display yield curve. """

        plt.figure(figsize=(12, 6))
        plt.title(title)
        bond_ylds_scaled = scale(self._ylds, 100.0)
        plt.plot(self._yearsToMaturity, bond_ylds_scaled, 'o')
        plt.xlabel('Time to Maturity (years)')
        plt.ylabel('Yield To Maturity (%)')

        tmax = np.max(self._yearsToMaturity)
        t = np.linspace(0.0, int(tmax+0.5), 100)

        yld = self.interpolatedYield(t)
        yld = scale(yld, 100.0)
        plt.plot(t, yld, label=str(self._curveFit))
        plt.legend(loc='lower right')
        plt.ylim((min(yld)-0.3, max(yld)*1.1))
        plt.grid(True)

###############################################################################

    def __repr__(self):
        s = labelToString("OBJECT TYPE", type(self).__name__)
        s += labelToString("SETTLEMENT DATE", self._settlement_date)
        s += labelToString("BOND", self._bonds)
        s += labelToString("YIELDS", self._ylds)
        s += labelToString("CURVE FIT", self._curveFit)
        return s

###############################################################################

    def _print(self):
        """ Simple print function for backward compatibility. """
        print(self)

##############################################################################
