''' Handles basic trend analysis for the given data '''
#import pandas as pd
#import seaborn as sns
#import seaborn.objects as so
import time                                         # for use in condition description
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
    if trend.positive_trend:
        trend.direction = "up"
    if trend.slope < 0:
        trend.direction = "down"
    if trend.slope > 0.25 or trend.slope < -0.25:
        trend.steep = True
    else:
        trend.steep = False

    return trend

def process_weather(weather, out):
    """ Review hourly data and return relevant a string describing the day's weather"""
    temp_list = []
    humid_list = []
    press_list = []
    precip_list = []
    clouds_list = []

    for hour in weather.hourly:
        temp_list.append(hour.temp_raw)
        humid_list.append(hour.humidity_raw)
        press_list.append(hour.pressure_raw)
        precip_list.append(hour.pop_raw)
        clouds_list.append(hour.clouds_raw)

    # Create a dictionary with the lists
    data = {
        'Temperature': temp_list,
        'Humidity': humid_list,
        'Pressure': press_list,
        'Precipitation': precip_list,
        'Clouds': clouds_list
    }

    # Create a DataFrame from the dictionary
    #df = pd.DataFrame(data)

    # Plot the dataset using seaborn
    #plot = sns.lineplot(x="hour",y="value",hue="region",style="event",data=df)
    #so.Lines.plot(plot)
    #sns.save("plot.png")

    temp_trend = identify_trend(temp_list)
    humid_trend = identify_trend(humid_list)
    press_trend = identify_trend(press_list)
    precip_trend = identify_trend(precip_list)
    clouds_trend = identify_trend(clouds_list)

    out.logger.debug(f"Temperature List: {temp_list}")
    out.logger.debug(f"Temperature Trend: {temp_trend.direction}")
    out.logger.debug(f"Temp Trend R Value: {temp_trend.r_value}")
    out.logger.debug(f"Temp Trend Slope: {temp_trend.slope}")

    out.logger.debug(f"Humidity List: {humid_list}")
    out.logger.debug(f"Humidity Trend: {humid_trend.direction}")
    out.logger.debug(f"Humidity Trend R Value: {humid_trend.r_value}")
    out.logger.debug(f"Humidity Trend Slope: {humid_trend.slope}")

    out.logger.debug(f"Pressure List: {press_list}")
    out.logger.debug(f"Pressure Trend: {press_trend.direction}")
    out.logger.debug(f"Pressure Trend R Value: {press_trend.r_value}")
    out.logger.debug(f"Pressure Trend Slope: {press_trend.slope}")

    out.logger.debug(f"Precipitation List: {precip_list}")
    out.logger.debug(f"Precipitation Trend: {precip_trend.direction}")
    out.logger.debug(f"Precipitation Trend R Value: {precip_trend.r_value}")
    out.logger.debug(f"Precipitation Trend Slope: {precip_trend.slope}")

    use_default_string = False
    today_string =""
    temp_string = ""
    humid_string = ""
    press_string = ""
    precip_string = ""
    clouds_string = ""
    qualifier_string = ""

    min_temp = min(temp_list)
    max_temp = max(temp_list)

    if temp_trend.slope < 0.25:
        if min_temp >= 90:
            temp_string = " stay ridiculously hot,"
        if min_temp <= 89 and max_temp >= 90:
            temp_string = " stay hot,"
        if min_temp >= 71 and max_temp <= 89:
            temp_string = " stay warm,"
        if min_temp >= 60 and max_temp <= 70:
            temp_string = " stay temperate,"
        if min_temp >= 40 and max_temp <= 60:
            temp_string = " stay cool,"
        if min_temp >= 32 and max_temp <= 40:
            temp_string = " stay above freezing,"
        if min_temp <= 32 and max_temp >= 35:
            temp_string = " drop below freezing,"
        if max_temp <= 32:
            temp_string = " stay below freezing,"
        if max_temp <= 0:
            temp_string = " stay ridiculously cold,"

        ### Ensure that there's always a temp_string if the trend is flat
        if temp_list == "":
            if min_temp >= 30:
                temp_string = " stay cold,"
            if min_temp >= 50:
                temp_string = " stay cool,"
            if min_temp >= 70:
                temp_string = " stay warm,"

    if temp_trend.steep or humid_trend.steep or press_trend.steep or precip_trend.steep:
        out.logger.info("Steep trend detected")

        if temp_trend.steep:
            if temp_trend.direction == "up":
                temp_string += " heat up"
            else:
                temp_string += " be cooler"
        if temp_string == "":
            temp_string = " maintain temperature"

        if humid_trend.steep:
            if humid_trend.direction == "up":
                humid_string += " with rising humidity"
            else:
                humid_string += " with falling humidity"

        if press_trend.steep:
            if press_trend.direction == "up":
                press_string += ", rising pressure"
            else:
                press_string += ", falling pressure"

        if precip_trend.steep:
            if precip_trend.direction == "down":
                precip_string += " and drying off"

        if clouds_trend.steep:
            if clouds_trend.direction == "up":
                clouds_string += " and cloud over"
            else:
                clouds_string += ", with fewer clouds"
    else:
        use_default_string = True
        today_string = "Current conditions will continue for the rest of"

    ### Conditionals for weather descriptions
    use_condition_string = False
    condition_string =""
    summary = weather.daily[0].summary
    if "storm" in summary:
        use_condition_string = True
        condition_string = " storms"

    if "snow" in summary:
        use_condition_string = True
        condition_string = " snow"

    if "rain" in summary:
        use_condition_string = True
        condition_string = " rain"

    if "heavy" in summary:
        qualifier_string = " heavy"

    if "light" in summary:
        qualifier_string = " light"

    day_text = " Today"
    if time.localtime().tm_hour >= 12:
        day_text = " This afternoon"
    if time.localtime().tm_hour >= 18:
        day_text = " This evening"
    if time.localtime().tm_hour >= 21:
        day_text = " Tonight"

    if use_default_string:
        lowercase_day_text = day_text.lower()
        today_string += f"{lowercase_day_text}"
    else:
        be_text = f"{temp_string}{humid_string}{press_string}{precip_string}{clouds_string}"
        today_string = f"{day_text} will{be_text}"

    if use_condition_string:
        today_string += f", with{qualifier_string}{condition_string}."
    else:
        today_string += "."

    return today_string
