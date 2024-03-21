''' Handles basic trend analysis for the given data '''

import numpy as np                                  # for linear regression
from sklearn.linear_model import LinearRegression   # for trend analysis
                                                    #   https://scikit-learn.org/stable/install.html
                                                    #   pip3 install scikit-learn

class TrendInfo:
    """ Custom object to store the trend information """
    def __init__(self):
        self.trend = None
        self.slope = None
        self.intercept = None
        self.r_value = None
        self.positive_trend = None
        self.direction = None
        self.steep = None
        self.no_slope = None

def identify_trend(data_list):
    """ Identify the trending direction of the given attribute """
    i = 0
    x = []
    y = data_list

    for iteration in data_list:
        i += 1
        x.append(i)
        #print(f"x: {i}, y: {iteration}")

    x_array = np.array(x)
    reshaped_x = x_array.reshape(-1, 1)

    model = LinearRegression().fit(reshaped_x, y)

    trend = TrendInfo()

    trend.slope = model.coef_
    trend.intercept = model.intercept_
    trend.r_value = model.score(reshaped_x, y)
    trend.no_slope = trend.slope == 0
    trend.positive_trend = trend.slope > 0
    trend.direction = "up" if trend.positive_trend else "down"
    if trend.slope > 2 or trend.slope < -2:
        trend.steep = True
    else:
        trend.steep = False

    return trend