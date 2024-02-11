### This module is responsible for rendering the weather data to an image using PIL and displaying it on the e-ink display

import imgkit                                           # for html to image conversion
from html2image import Html2Image                       # alternate for html to image conversion
import traceback                                        # for error handling
import sys                                              # for error handling
import time                                             # for time formatting   
from inky.auto import auto                              # for working with the e-ink display
from PIL import Image,ImageDraw,ImageFont, ImageFilter  # for rendering via PIL

def render_pil(city_one_name, city_one_weather, out, city_two_name = None, city_two_weather = None):
    """ Render text to image using PIL """
    """ Urbanist-Thin.ttf,          Urbanist-ThinItalic.ttf
        Urbanist-ExtraLight.ttf,    Urbanist-ExtraLightItalic.ttf
        Urbanist-Light.ttf,         Urbanist-LightItalic.ttf
        Urbanist-Regular.ttf,       Urbanist-Italic.ttf
        Urbanist-Medium.ttf,        Urbanist-MediumItalic.ttf
        Urbanist-SemiBold.ttf,      Urbanist-SemiBoldItalic.ttf
        Urbanist-Bold.ttf,          Urbanist-BoldItalic.ttf
        Urbanist-ExtraBold.ttf,     Urbanist-ExtraBoldItalic.ttf
        Urbanist-Black.ttf,         Urbanist-BlackItalic.ttf
    """
    out.logger.info("Rendering weather data to image using PIL")
    
    try:
        max_width = 800
        max_height = 480
        canvas = Image.new('RGB', (max_width, max_height), "white")
        draw = ImageDraw.Draw(canvas)
        
        date = time.strftime("%B %-d", time.localtime())
        weekday = time.strftime("%a", time.localtime())
        load_time = time.strftime("%-I:%M %p", time.localtime())

        header_one = ImageFont.truetype("/usr/share/fonts/truetype/Urbanist-ExtraBold.ttf", 64, encoding="unic")
        header_two = ImageFont.truetype("/usr/share/fonts/truetype/Urbanist-SemiBoldItalic.ttf", 35, encoding="unic")
        forecast_header = ImageFont.truetype("/usr/share/fonts/truetype/Urbanist-SemiBold.ttf", 25, encoding="unic")
        forecast_city = ImageFont.truetype("/usr/share/fonts/truetype/Urbanist-ExtraBold.ttf", 45, encoding="unic")
        forecast_paragraph = ImageFont.truetype("/usr/share/fonts/truetype/Urbanist-Bold.ttf", 11, encoding="unic")
        paragraph = ImageFont.truetype("/usr/share/fonts/truetype/Urbanist-Regular.ttf", 20, encoding="unic")
        big_number = ImageFont.truetype("/usr/share/fonts/truetype/Urbanist-Black.ttf", 64, encoding="unic")
        mid_number = ImageFont.truetype("/usr/share/fonts/truetype/Urbanist-Bold.ttf", 16, encoding="unic")
        subtext = ImageFont.truetype("/usr/share/fonts/truetype/Urbanist-Italic.ttf", 16, encoding="unic")

        dummy_width, big_number_height = big_number.getsize("Ag") # Use 'Ag' to cover normal full range above and below the line
        dummy_width, header_one_height = header_one.getsize("Ag")
        dummy_width, header_two_height = header_two.getsize("Ag")
        dummy_width, forecast_header_height = forecast_header.getsize("Ag")
        time_stamp = f"CONDITIONS AS OF {load_time}"
        time_stamp_width, paragraph_height = paragraph.getsize(time_stamp) # Use an actual string to determine the x position for right-justification on the canvas

        ### Draw the [day of the week], [month] [day] header, top-left
        date_stamp = f"{weekday}, {date}".upper()
        draw.text((5, 1), date_stamp, 'blue', header_two)

        ### Draw the [time] header, top-right, right-justified
        draw.text((max_width - time_stamp_width - 5, 1), time_stamp, 'blue', paragraph)

        def draw_city_data(x_position, city_name, weather_data, draw, y_position, city_number = 1):
            """ Draw the city name and weather data """

            ### NAME ###
            city_name = city_name.upper()
            out.logger.debug(f"Y position: {y_position}: {city_name}")
            draw.text((x_position, y_position), f"{city_name}", 'red', header_one)
            y_position += header_one_height - 20
            
            ### TEXT SUMMARY ###
            out.logger.debug(f"Y position: {y_position}: {weather_data.daily[0].summary}")
            draw.text((x_position, y_position), f"{weather_data.daily[0].summary}", 'black', paragraph)
            y_position += 20

            ### ICON ###
            icon_file = f'icons/{weather_data.current.weather.icon}.png'
            img = Image.open(icon_file)

            icon_width, icon_height = img.size
            img.resize((icon_width * 2, icon_height * 2))
            
            img.filter(ImageFilter.EDGE_ENHANCE_MORE)

            img_x_position = int(x_position + 400 - icon_width * 1.5)
            img_y_position = int(y_position + icon_height / 1.8)

            canvas.paste(img, (img_x_position, img_y_position))

            img_x_position = int(x_position + 400 - (icon_width / 2))

            draw.text((img_x_position, img_y_position + 60), f"{weather_data.current.weather.description}", 'orange', subtext, align="center")

            ### TODO ###

            ### Conditional logic for different weather conditions:
            ###     If current condition is clear, pull weather.current.uvi
            ###     If current condition is cloudy, pull weather.current.clouds (%), if rain/snow: weather.current.rain (/ snow) (mm/h)
            ###     If current condition is foggy, pull weather.current.visibility (meters)

            ### Icons based on season/temperature
            ###     https://www.flaticon.com/packs/search?word=weather&color=color&shape=lineal-color&order_by=4
            ###
            ###     winter: https://www.flaticon.com/packs/weather-561?word=weather
            ###     spring:
            ###     summer: https://www.flaticon.com/packs/weather-157?word=weather
            ###     fall: 
            ###     hot/normal/cold

            ############
            
            ### BIG TEMP ###
            def temp_color(temp):
                if temp < 50:
                    return 'blue'
                if temp > 80:
                    return 'red'
                return 'green'
            
            color = temp_color(weather_data.current.temp)

            current_temp = "{:.0f}".format(weather_data.current.temp)
            out.logger.debug(f"Y position: {y_position}: {current_temp}°F")
            draw.text((x_position, y_position), f"{current_temp}°F", color, big_number)
            y_position += big_number_height -20

            ### HIGH/LOW TEMP ###
            daily_max = "{:.0f}".format(weather_data.daily[0].temp.max)
            daily_min = "{:.0f}".format(weather_data.daily[0].temp.min)
            out.logger.debug(f"Y position: {y_position}: {daily_max} / {daily_min}°F")
            draw.text((x_position, y_position), f"↑{daily_max} / ↓{daily_min}°F", color, header_two)
            y_position += header_two_height - 10

            ### FEELS LIKE ###
            daily_feels = "{:.0f}".format(weather_data.current.feels_like)
            out.logger.debug(f"Y position: {y_position}: Feels like: {daily_feels}°F")  
            draw.text((x_position, y_position), f"Feels like: {daily_feels}°F", 'black', paragraph)
            y_position += 20

            ### HUMIDITY ###
            out.logger.debug(f"Y position: {y_position}: Humidity: {weather_data.current.humidity}%")
            draw.text((x_position, y_position), f"Humidity: {weather_data.current.humidity}%", 'black', paragraph)
            y_position += 20

            ### WIND SPEED AND DIRECTION ###
            def get_compass_direction(degrees):
                directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
                index = round(degrees / 22.5) % 16
                return directions[index]
            daily_wind = "{:.0f}".format(weather_data.current.wind_speed)
            out.logger.debug(f"Y position: {y_position}: Wind Speed: {daily_wind}mph {weather_data.daily[0].wind_deg}°")
            draw.text((x_position, y_position), f"Wind Speed: {daily_wind}mph {get_compass_direction(weather_data.daily[0].wind_deg)}", 'black', paragraph)

            ### DAILY FORECAST ###
            if city_number == 1:
                y_position = max_height / 2 + 50

                for day in weather_data.daily: # Draw the header
                    x_position += int(max_width / 8)
                    date = time.strftime('%a %d', time.localtime(day.dt))
                    draw.text((x_position, y_position), f"{date}", 'red', forecast_header)

                y_position += forecast_header_height + 5
            else:
                y_position = max_height / 2 + 150

            city_name_trunc = city_name[:3]
            x_position = 5
            row = y_position
            counter = 0
            for day in weather_data.daily:
                y_position = row

                counter += 1
                if counter == 1:
                    y_position = row
                    draw.text((x_position, y_position), f"{city_name_trunc}", 'red', forecast_city)
                
                x_position += int(max_width / 8)

                date = time.strftime('%a %d', time.localtime(day.dt))
                pop = day.pop * 100

                max_color = temp_color(day.temp.max)
                min_color = temp_color(day.temp.min)
                
                ### MAX TEMP ###
                daily_max = "{:.0f}".format(day.temp.max)
                text = f"{daily_max}"
                draw.text((x_position, y_position), text, max_color, mid_number)
                text_width, text_height = mid_number.getsize(text)

                ### MIN TEMP ###
                daily_min = "{:.0f}".format(day.temp.min)
                text = f"/{daily_min}°F"
                draw.text((x_position + text_width, y_position), text, min_color, mid_number)
                text_width, text_height = mid_number.getsize(text)

                ### WEATHER DESCRIPTION ###
                text = f"{day.weather.description} "
                y_position += text_height
                draw.text((x_position, y_position), text, 'green', forecast_paragraph)
                text_width, text_height = forecast_paragraph.getsize(text)

                ### POP ###
                text = f"{pop}% precip."
                y_position += text_height
                draw.text((x_position, y_position), text, 'green', forecast_paragraph)
                text_width, text_height = forecast_paragraph.getsize(text)

                ### WIND SPEED ###
                daily_wind = "{:.0f}".format(day.wind_speed)
                text = f"{daily_wind}mph"
                y_position += text_height
                draw.text((x_position, y_position), text, 'green', forecast_paragraph)

                #print(f'{date} {day.temp.max} / {day.temp.min}°F {day.weather.description}, {pop}% chance of precipitation, {day.wind_speed}mph wind')

        ### Draw the city one name and establish the initial y position for the remaining text
        y_position = header_one_height - 25
        draw_city_data(5, city_one_name, city_one_weather, draw, y_position)

        if city_two_weather:
            draw_city_data(400, city_two_name, city_two_weather, draw, y_position, 2)

        # save the blank canvas to a file
        canvas.save("pil-text.png", "PNG")

        inky = auto(ask_user=True, verbose=True)
        saturation = 1

        image = Image.open("pil-text.png")
        resizedimage = image.resize(inky.resolution)

        inky.set_image(resizedimage, saturation=saturation)
        canvas.show()
        inky.show()
    except Exception:
        out.logger.critical("Error rendering weather data to image using PIL")
        out.logger.critical(traceback.format_exc())
        sys.exit
