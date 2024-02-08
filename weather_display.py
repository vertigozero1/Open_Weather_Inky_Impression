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

## Custom Modules
import modules.initialization as init   # handles configuration and logging
import modules.query_weather as owAPI   # handles querying the OpenWeather API
import modules.get_image as img         # handles rendering HTML to image

## Main Program
config = init.get_config()
out = init.start_logging(config.log_evel)

startTime = time.time()
startDatetime = datetime.fromtimestamp(startTime)
cleanStartTime = startDatetime.strftime('%Y-%m-%d %H:%M:%S')

out.logger.info("Starting weatherDisplay.py at %s", cleanStartTime)
out.logger.debug(config)

out.logger.info("Getting weather data for %s", config.city_one_name)
city1Weather = owAPI.get_weather_data(
    config.api_key, 
    config.units, 
    config.city_one_lat, 
    config.city_one_lon, 
    out)

out.logger.info("Getting weather CSS for %s", config.city_one_name)
html = owAPI.generate_weather_html(city1Weather, out)

if config.render_method == "imgkit":
    out.logger.debug("Rendering HTML to image using imgkit")
    img.render_imgkit(html, out)
elif config.render_method == "html2image":
    out.logger.debug("Rendering HTML to image using html2image")
    img.render_html2image(html, out)

if config.mode == "dual":
    out.logger.info("Dual mode enabled in config.ini")
    out.logger.info("Getting weather data for %s", config.city_two_name)
    city2Weather = owAPI.get_weather_data(
        config.api_key, 
        config.units, 
        config.city_two_lat, 
        config.city_two_lon, 
        out)

    out.logger.info("Getting weather CSS for %s", config.city_two_name)
    css2 = owAPI.generate_weather_html(city2Weather, out)
    out.logger.debug("CSS2: %s", css2)

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

