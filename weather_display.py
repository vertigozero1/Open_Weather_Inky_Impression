"""
  ┳  ┓   ┏┓      ┓ ┏     ┓       ┏┓    •    
┏┓┃┏┓┃┏  ┃┃┏┓┏┓┏┓┃┃┃┏┓┏┓╋┣┓┏┓┏┓  ┗┓╋┏┓╋┓┏┓┏┓
┗ ┻┛┗┛┗  ┗┛┣┛┗ ┛┗┗┻┛┗ ┗┻┗┛┗┗ ┛   ┗┛┗┗┻┗┗┗┛┛┗
-----------┛--------------------------------                              
for Raspberry Pi and Pimoroni Inky Impression 7.3" e-ink display
"""
### Community Libraries
import time                     # for getting the current time
from datetime import datetime   # for converting the time to human-readable format
import traceback                # for error handling
import sys                      # for error handling

### Custom Modules
import modules.initialization as init   # handles configuration and logging
import modules.weather as weather   # handles querying the OpenWeather API
import modules.get_image as img         # handles rendering HTML to image
import modules.inky as inky             # handles rendering image to e-ink display

### Main Program

## Initialize
config = init.get_config()
out = init.start_logging(config.log_level)

startTime = time.time()
startDatetime = datetime.fromtimestamp(startTime)
cleanStartTime = startDatetime.strftime('%Y-%m-%d %H:%M:%S')

city_one_name = config.city_one_name

out.logger.info("Starting weatherDisplay.py at %s", cleanStartTime)
out.logger.debug(config)

## Get weather data
out.logger.info("Getting weather data for %s", city_one_name)
city_one_data = weather.get_data(
    config.api_key, 
    config.units, 
    config.city_one_lat, 
    config.city_one_lon, 
    out)
weather_one = weather.create_data_object(city_one_name, city_one_data)
weather.log_data(weather_one, out)

weather_two = None
if config.mode == "dual":
    city_two_name = config.city_two_name
    city_two_data = weather.get_data(
        config.api_key, 
        config.units, 
        config.city_two_lat, 
        config.city_two_lon, 
        out)
    weather_two = weather.create_data_object(city_two_name, city_two_data)
    weather.log_data(weather_two, out)

### Call render module based on config.ini setting
### If render_method is PIL, HTML will not be necessary
if config.render_method == "pil":
    out.logger.debug("Using PIL render method, based on config.ini setting")
    out.logger.debug("Rendering HTML to image using PIL")
    img.render_pil(city_one_name, city_one_data, out, city_two_name, city_two_data)
else:
    out.logger.info("Getting weather HTML for %s", city_one_name)
    if config.mode != "dual":
        out.logger.debug("Single mode enabled in config.ini")
        out.logger.info("Getting weather data for %s", city_one_name)
        html = weather.generate_html(city_one_name, city_one_data, out)
    else:
        out.logger.info("Dual mode enabled in config.ini; also getting weather data for %s", city_two_name)
        city_two_data = weather.get_data(
            config.api_key, 
            config.units, 
            config.city_two_lat, 
            config.city_two_lon, 
            out)
        html = weather.generate_html(city_one_name, city_one_data, out, city_two_name, city_two_data)

### The remaining options require HTML to be written to a file
if config.render_method == "imgkit":
    try:
        out.logger.debug("Using imgkit render method, based on config.ini setting")
        out.logger.debug("Writing HTML to file")
        with open('weather.html', 'w') as file:
            file.write(html)
    except Exception:
        out.logger.critical("Error writing HTML to file")
        out.logger.critical(traceback.format_exc())
        sys.exit
    out.logger.debug("Rendering HTML to image using imgkit")
    img.render_imgkit(out)
elif config.render_method == "html2image":
    out.logger.debug("Using html2image render method, based on config.ini setting") 
    out.logger.debug("Rendering HTML to image using html2image")
    img.render_html2image(html, out)
    inky.render_image(out)

endTime = time.time()
duration = endTime - startTime
formattedDuration = "{:.2f}".format(duration)

out.logger.info("Ending weatherDisplay.py at %s", endTime)
out.logger.info("Duration: %s seconds", formattedDuration)
out.logger.info("=======================")