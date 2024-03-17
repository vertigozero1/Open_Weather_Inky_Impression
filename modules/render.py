""" This module is responsible for rendering the weather data 
 to an image using PIL and displaying it on the e-ink display"""

import traceback                                        # for error handling
import sys                                              # for error handling
import time                                             # for time formatting
from inky.auto import auto                              # for working with the e-ink display
                                                        #   `pip3 install inky[rpi,example-depends]`
from PIL import Image,ImageDraw,ImageFont,ImageFilter  # for rendering via PIL `pip3 install pillow`


def get_size(font, text):
    """Get the size of the text using getbbox() since getsize() is deprecated in Pillow 8.0.0.
    https://pillow.readthedocs.io/en/stable/releasenotes/8.0.0.html#deprecations

    Args:
        font (Font): The font used for rendering the text.
        text (str): The text to measure the size of.

    Returns:
        tuple: A tuple containing the width and height of the text.
    """
    left, top, right, bottom = font.getbbox(text)
    text_width, text_height = right - left, bottom - top
    return text_width, text_height


def render_pil(city_one_name, city_one_weather, out, city_two_name = None, city_two_weather = None):
    """
    Render text to image using PIL.

    Args:
        city_one_name (str): The name of the first city.
        city_one_weather: The weather data for the first city.
        out: The output object.
        city_two_name (str, optional): The name of the second city. Defaults to None.
        city_two_weather (optional): The weather data for the second city. Defaults to None.
    """
    # The Urbanist font family is used for rendering the text:
    #     Urbanist-Thin.ttf,          Urbanist-ThinItalic.ttf
    #     Urbanist-ExtraLight.ttf,    Urbanist-ExtraLightItalic.ttf
    #     Urbanist-Light.ttf,         Urbanist-LightItalic.ttf
    #     Urbanist-Regular.ttf,       Urbanist-Italic.ttf
    #     Urbanist-Medium.ttf,        Urbanist-MediumItalic.ttf
    #     Urbanist-SemiBold.ttf,      Urbanist-SemiBoldItalic.ttf
    #     Urbanist-Bold.ttf,          Urbanist-BoldItalic.ttf
    #     Urbanist-ExtraBold.ttf,     Urbanist-ExtraBoldItalic.ttf
    #     Urbanist-Black.ttf,         Urbanist-BlackItalic.ttf
    out.logger.info("Rendering weather data to image using PIL")

    try:
        max_width = 800
        max_height = 480
        canvas = Image.new('RGB', (max_width, max_height), "white")
        draw = ImageDraw.Draw(canvas)

        date = time.strftime("%B %-d", time.localtime())
        weekday = time.strftime("%a", time.localtime())
        load_time = time.strftime("%-I:%M %p", time.localtime())

        header_one = ImageFont.truetype(
            "/usr/share/fonts/truetype/Urbanist-ExtraBold.ttf", 64, encoding="unic")
        header_two = ImageFont.truetype(
            "/usr/share/fonts/truetype/Urbanist-SemiBoldItalic.ttf", 35, encoding="unic")
        forecast_header = ImageFont.truetype(
            "/usr/share/fonts/truetype/Urbanist-SemiBold.ttf", 25, encoding="unic")
        forecast_city = ImageFont.truetype(
            "/usr/share/fonts/truetype/Urbanist-ExtraBold.ttf", 45, encoding="unic")
        forecast_paragraph = ImageFont.truetype(
            "/usr/share/fonts/truetype/Urbanist-Bold.ttf", 11, encoding="unic")
        paragraph = ImageFont.truetype(
            "/usr/share/fonts/truetype/Urbanist-Regular.ttf", 20, encoding="unic")
        big_number = ImageFont.truetype(
            "/usr/share/fonts/truetype/Urbanist-Black.ttf", 64, encoding="unic")
        mid_number = ImageFont.truetype(
            "/usr/share/fonts/truetype/Urbanist-Bold.ttf", 16, encoding="unic")
        subtext = ImageFont.truetype(
            "/usr/share/fonts/truetype/Urbanist-Italic.ttf", 16, encoding="unic")

        # Use 'Ag' to cover normal full height range above and below the line
        dummy_width, big_number_height = get_size(big_number, "Ag")
        dummy_width, header_one_height = get_size(header_one, "Ag")
        dummy_width, header_two_height = get_size(header_two, "Ag")
        dummy_width, forecast_header_height = get_size(forecast_header, "Ag")

        time_stamp = f"CONDITIONS AS OF {load_time}"
        # Use an actual string to determine the x position for right-justification on the canvas
        time_stamp_width, dummy_height = get_size(paragraph, time_stamp)

        ### Draw the [day of the week], [month] [day] header, top-left
        date_stamp = f"{weekday}, {date}".upper()
        draw.text((5, 1), date_stamp, 'blue', header_two)

        ### Draw the [time] header, top-right, right-justified
        draw.text((max_width - time_stamp_width - 5, 1), time_stamp, 'blue', paragraph)

        def draw_city_data(x_position, city_name, weather_data, draw, y_position, city_number=1):
            """
            Draw the city name, weather data, and forecast information on the canvas.

            Parameters:
            - x_position (int): The x-coordinate position to start drawing.
            - city_name (str): The name of the city.
            - weather_data (WeatherData): An object containing weather data.
            - draw (ImageDraw): The ImageDraw object used for drawing on the canvas.
            - y_position (int): The y-coordinate position to start drawing.
            - city_number (int, optional): The number of the city. Defaults to 1.

            Returns:
            None
            """
            ### NAME ###
            city_name = city_name.upper()
            out.logger.debug(f"Y position: {y_position}: {city_name}")
            draw.text((x_position, y_position), f"{city_name}", 'red', header_one)
            y_position += header_one_height

            ### TEXT SUMMARY ###
            out.logger.debug(f"Y position: {y_position}: {weather_data.daily[0].summary}")
            summary_position = x_position, y_position
            draw.text((summary_position), f"{weather_data.daily[0].summary}", 'black', paragraph)
            y_position += 20

            ### ICON ###
            icon_file = f'icons/{weather_data.current.weather.icon}.png'
            img = Image.open(icon_file)

            icon_width, icon_height = img.size
            img.resize((icon_width * 3, icon_height * 3))

            img.filter(ImageFilter.EDGE_ENHANCE_MORE)

            img_x_position = int(x_position + 400 - icon_width * 2.5)
            img_y_position = int(y_position + icon_height / 1.8)
            img_position = img_x_position, img_y_position

            canvas.paste(img, img_position)

            img_x_position = int(x_position + 400 - icon_width * 2.5)

            description_position = img_x_position - 20, img_y_position + 40
            draw.text(description_position, f"{weather_data.current.weather.description}", 'black', subtext)

            ### TODO ###

            ### Conditional logic for different weather conditions:
            ###     If current condition is clear, pull weather.current.uvi
            ###     If current condition is cloudy, pull weather.current.clouds (%),
            ###             if rain/snow: weather.current.rain (/ snow) (mm/h)
            ###     If current condition is foggy, pull weather.current.visibility (meters)

            ### Icons based on season/temperature
            ###     https://www.flaticon.com/packs/search?
            ###         word=weather&color=color&shape=lineal-color&order_by=4
            ###
            ###     winter: https://www.flaticon.com/packs/weather-561?word=weather
            ###     spring:
            ###     summer: https://www.flaticon.com/packs/weather-157?word=weather
            ###     fall:
            ###     hot/normal/cold

            ############

            def temp_color(temp):
                """
                Determines the color based on the temperature.

                Parameters:
                temp (float or int): The temperature value.

                Returns:
                str: The color corresponding to the temperature.

                """
                try:
                    temp = int(float(temp))
                except ValueError:
                    return 'green'

                if temp < 30:
                    color = 'cyan'
                if temp < 40:
                    color = 'lightblue'
                if temp < 50:
                    color = 'deepskyblue'
                if temp < 60:
                    color = 'blue'
                if temp > 70:
                    color = 'indianred'
                if temp > 80:
                    color = 'darkorange'
                if temp > 90:
                    color = 'darkred'
                if temp > 100:
                    color = 'red'
                else:
                    color = 'green'
                return color

            def type_int(value):
                """
                Ensure that the value is not typed as string.

                Parameters:
                value (any): The value to be converted.

                Returns:
                int: The converted integer value. If the conversion fails, returns 0.
                """
                try:
                    return int(value)
                except ValueError:
                    return 0

            ### BIG TEMP ###
            color = temp_color(weather_data.current.temp)

            current_temp = f"{type_int(weather_data.current.temp):.0f}°F"
            out.logger.debug(f"Y position: {y_position}: {current_temp}")
            draw.text((x_position, y_position), f"{current_temp}", color, big_number)
            y_position += big_number_height

            feels_like_x_position = x_position

            ### HIGH/LOW TEMP ###
            section_font = header_two

            daily_max_int = type_int(weather_data.daily[0].temp.max)
            daily_max_color = temp_color(daily_max_int)
            daily_max_string = f"↑{daily_max_int:.0f}"
            daily_max_width, daily_max_height = get_size(section_font, daily_max_string)

            draw.text((x_position, y_position), daily_max_string, daily_max_color, section_font)
            x_position += daily_max_width

            separator = " / "
            separator_width, separator_height = get_size(section_font, separator)
            draw.text((x_position, y_position), separator, 'black', section_font)
            x_position += separator_width
            
            daily_min_int = type_int(weather_data.daily[0].temp.min)
            daily_min_color = temp_color(daily_min_int)
            daily_min_string = f"↓{daily_min_int:.0f}°F"

            draw.text((x_position, y_position), daily_min_string, daily_min_color, section_font)

            out.logger.debug(f"Y position: {y_position}: {daily_max_string}{daily_min_string}")

            y_position += header_two_height

            ### FEELS LIKE ###
            x_position = feels_like_x_position
            daily_feels_int = type_int(weather_data.current.feels_like)
            daily_feels_string = f"{daily_feels_int:.0f}°F"
            out.logger.debug(f"Y position: {y_position}: Feels like: {daily_feels_string}")
            draw.text((x_position, y_position), f"Feels like: {daily_feels_string}", 'black', paragraph)
            y_position += 20

            ### HUMIDITY ###
            humidity = f"{type_int(weather_data.current.humidity)}%"
            out.logger.debug(f"Y position: {y_position}: Humidity: {humidity}")
            draw.text((x_position, y_position), f"Humidity: {humidity}", 'black', paragraph)
            y_position += 20

            ### WIND SPEED AND DIRECTION ###
            wind_speed = type_int(weather_data.current.wind_speed)
            daily_wind = f"{wind_speed:.0f}mph {weather_data.current.wind_dir}"
            out.logger.debug(f"Y position: {y_position}: Wind Speed: {daily_wind}")
            draw.text((x_position, y_position), f"Wind Speed: {daily_wind}", 'black', paragraph)

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
                section_font = mid_number
                daily_max = f"{type_int(day.temp.max):.0f}"
                text = f"{daily_max}"
                draw.text((x_position, y_position), text, max_color, section_font)
                text_width, text_height = get_size(section_font, text)

                ### MIN TEMP ###
                text = f"/{type_int(day.temp.min):.0f}°F"
                draw.text((x_position + text_width, y_position), text, min_color, section_font)
                dummy_width, text_height = get_size(section_font, text)

                ### WEATHER DESCRIPTION ###
                section_font = forecast_paragraph
                text = f"{day.weather.description}"
                y_position += text_height
                draw.text((x_position, y_position), text, 'green', section_font)
                text_width, text_height = get_size(section_font, text)

                ### POP ###
                text = f"{type_int(pop)}% precip."
                y_position += text_height
                draw.text((x_position, y_position), text, 'green', section_font)
                text_width, text_height = get_size(section_font, text)

                ### WIND SPEED ###
                text = f"{type_int(day.wind_speed):.0f}mph"
                y_position += text_height
                draw.text((x_position, y_position), text, 'green', section_font)

        ### Draw the city one name and establish the initial y position for the remaining text
        y_position = header_one_height - 35
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
        sys.exit()
