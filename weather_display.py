"""
  ┳  ┓   ┏┓      ┓ ┏     ┓       ┏┓    •    
┏┓┃┏┓┃┏  ┃┃┏┓┏┓┏┓┃┃┃┏┓┏┓╋┣┓┏┓┏┓  ┗┓╋┏┓╋┓┏┓┏┓
┗ ┻┛┗┛┗  ┗┛┣┛┗ ┛┗┗┻┛┗ ┗┻┗┛┗┗ ┛   ┗┛┗┗┻┗┗┗┛┛┗
-----------┛--------------------------------                              
for Raspberry Pi and Pimoroni Inky Impression 7.3" e-ink display
"""
## Community Libraries
import time                     # for getting the current time
from datetime import datetime   # for converting the time to human-readable format
import traceback                # for error handling
import sys                      # for error handling

## Custom Modules
import modules.initialization as init   # handles configuration and logging
import modules.weather as weather   # handles querying the OpenWeather API
import modules.get_image as img         # handles rendering HTML to image
import modules.inky as inky             # handles rendering image to e-ink display

## Main Program
config = init.get_config()
out = init.start_logging(config.log_evel)

startTime = time.time()
startDatetime = datetime.fromtimestamp(startTime)
cleanStartTime = startDatetime.strftime('%Y-%m-%d %H:%M:%S')

out.logger.info("Starting weatherDisplay.py at %s", cleanStartTime)
out.logger.debug(config)

out.logger.info("Getting weather data for %s", config.city_one_name)
city_one_weather = weather.get_data(
    config.api_key, 
    config.units, 
    config.city_one_lat, 
    config.city_one_lon, 
    out)

out.logger.info("Getting weather HTML for %s", config.city_one_name)
if config.mode != "dual":
    out.logger.debug("Single mode enabled in config.ini")
    out.logger.info("Getting weather data for %s", config.city_one_name)
    html = weather.generate_html(config.city_one_name, city_one_weather, out)
else:
    out.logger.info("Dual mode enabled in config.ini; also getting weather data for %s", config.city_two_name)
    city_two_weather = weather.get_data(
        config.api_key, 
        config.units, 
        config.city_two_lat, 
        config.city_two_lon, 
        out)
    html = weather.generate_html(config.city_one_name, city_one_weather, out, config.city_two_name, city_two_weather)

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

#from inky.auto import auto # for working with the e-ink display
#from PIL import Image, ImageFont, ImageDraw # for working with images
#import time # for sleeping between requests
#import datetime # for getting the current time

