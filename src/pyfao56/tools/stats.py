"""
########################################################################
The stats.py module contains the Statistics class, which provides
several statistics that can be run for the entirety of the season. 
These calculations can be ran on any measured and modeled parameter. 

Calculations include Root Mean Square Error, Nash-Sutcliffe Efficiency, 
Linear Regression, and Bias. 

The stats.py module contains the following:
    Statistics - A class for calculating statistics over the season

10/12/2023 Initial Python functions developed by Tyler Pokoski, USDA-ARS
########################################################################
"""


# Import (public) python modules used in the code below
import pandas as pd
import numpy as np
import scipy
import math
from statistics import mean
from sklearn.metrics import mean_squared_error
from datetime import datetime as dt, timedelta
import hydroeval as he


class Statistics:
    
    def __init__(self, meas, modeled):
        """
        Calculate RSME, bias, and R-squared.
        
        Parameters
        ----------
        date : str
            'YYYY-DOY' for the date corresponding to the row of data.
        meas : List object
            List object containing measured data
        modeled: List object
            List object containing the simulated data for comparison

        Returns
        -------
        rmse : Root Mean Square Error, float
        bias : Bias between measured and simulated, float
        rsquare : The R-Squared value, float
        nse : Nash-Sutcliffe model efficiency coefficient, float
        """
        meas_check = self.all_identical(meas)
        modeled_check = self.all_identical(modeled)
        if meas_check == True:
            print('Measured values: ', meas)
        if modeled_check == True:
            print('Modeled values: ', modeled)
        if meas != modeled and meas_check==False and modeled_check==False:
            meas_mean = sum(meas) / len(meas)
            modeled_mean = sum(modeled)  / len(modeled)
            rmse = self.rmse(meas,modeled)
            bias = (modeled_mean - meas_mean)/meas_mean * 100
            res = scipy.stats.linregress(x=modeled, y=meas)
            rsquare = res.rvalue**2
            nse = self.nse(meas, modeled)
        else:
            #This is under the assumption that Mean = Modeled, therefore
            #the statistics would be perfect
            rmse = 0
            bias = 0
            rsquare = 1
            nse = 1
        return rmse, bias, rsquare, nse
    
    def all_identical(self, listx):
        """Returns True if all of the elements in the list are identical, 
        False otherwise."""
        for i in range(1, len(listx)):
            if listx[i] != listx[i - 1]:
                return False
        return True
    
    def rmse(self, meas, modeled):
        """
        Root Mean Square Error
        
        """
        differences = []
        for i in range(len(meas)):
            differences.append(meas[i] - modeled[i])

        # Square the differences.
        squared_differences = []
        for difference in differences:
            squared_differences.append(difference**2)
        # Calculate the mean of the squared differences.
        mean = sum(squared_differences) / len(squared_differences)
        # Take the square root of the mean.
        rmse = math.sqrt(mean)
        return rmse
    
    def nse(self, meas, modeled):
        """
        Nash-Sutcliffe Efficiency Coefficient
        The error variance of the modeled data divided by the variance
        of the observed data. By subtracting one by this ratio, the 
        result is a value that is highly similar to the model the closer
        the coefficient is to 1. 
        """
        meas_mean = mean(meas)                
        sse = sum([(meas[i] - modeled[i])**2 for i in range(len(meas))])
        sst = sum([(meas[i] - meas_mean)**2 for i in range(len(meas))])
        nse = 1 - (sse/sst)
        return nse
        
    
        
