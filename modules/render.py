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

def temp_color(input):
    """
    Determines the color based on the temperature.

    Parameters:
    temp (float or int): The temperature value.

    Returns:
    tuple: A tuple containing the color and icon name.
    """

    temp = type_int(input)

    icon_none = 'thermometer'
    icon_cold = 'thermometer_low'
    icon_moderate = 'thermometer_half'
    icon_hot = 'thermometer_high'
    icon_nope = 'thermometer_full'

    if temp < 39:
        color = 'cyan'
        icon = icon_cold
    elif 40 < temp < 49:
        color = 'lightblue'
        icon = icon_cold
    elif 50 < temp < 59:
        color = 'deepskyblue'
        icon = icon_moderate
    elif 60 < temp < 69:
        color = 'blue'
        icon = icon_moderate
    elif 70 < temp < 79:
        color = 'indianred'
        icon = icon_moderate
    elif 80 < temp < 89:
        color = 'darkorange'
        icon = icon_hot
    elif 90 < temp < 99:
        color = 'darkred'
        icon = icon_hot
    elif temp > 100:
        color = 'red'
        icon = icon_nope
    else:
        color = 'black'
        icon = icon_none
    return color, icon

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
            "/usr/share/fonts/truetype/Urbanist-Bold.ttf", 14, encoding="unic")
        paragraph = ImageFont.truetype(
            "/usr/share/fonts/truetype/Urbanist-Regular.ttf", 20, encoding="unic")
        big_number = ImageFont.truetype(
            "/usr/share/fonts/truetype/Urbanist-Black.ttf", 64, encoding="unic")
        mid_number = ImageFont.truetype(
            "/usr/share/fonts/truetype/Urbanist-Bold.ttf", 21, encoding="unic")
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
            draw.text((x_position, y_position), f"{city_name}", 'red', header_one, stroke_width=2, stroke_fill='black')
            y_position += header_one_height

            ### TEXT SUMMARY ###
            out.logger.debug(f"Y position: {y_position}: {weather_data.daily[0].summary}")
            summary_position = x_position, y_position
            draw.text((summary_position), f"{weather_data.daily[0].summary}", 'black', paragraph)
            y_position += 20

            ### CURRENT CONDITION ICON ###
            icon_file = f'icons/{weather_data.current.weather.icon}.png'

            try:
                img = Image.open(icon_file)
            except FileNotFoundError:
                img = Image.open('icons/unknown.png')

            icon_width, icon_height = img.size
            img.resize((icon_width * 3, icon_height * 3))

            img.filter(ImageFilter.EDGE_ENHANCE_MORE)

            img_x_position = int(x_position + 400 - icon_width * 2.5)
            img_y_position = int(y_position + icon_height / 1.8)
            img_position = img_x_position, img_y_position

            canvas.paste(img, img_position)

            ### DESCRIPTION ###
            description = f"{weather_data.current.weather.description}"
            description_width, description_height = get_size(subtext, description)
            img_x_midpoint = img_x_position + (icon_width / 2)
            img_y_bottom = img_y_position + icon_height
            description_position = img_x_midpoint - (description_width / 2), img_y_bottom + 5

            draw.text(description_position, description, 'black', subtext)

            ### THERMOMETER ICON ###
            temp = type_int(weather_data.current.temp)
            color, icon = temp_color(temp)
            out.logger.debug(f"Temperature variable type after type_int: {type(temp)}")

            out.logger.debug(f"temp: {temp}, color: {color}, icon: {icon}")

            icon_file = f'icons/{icon}.png'
            try:
                img = Image.open(icon_file)
            except FileNotFoundError:
                out.logger.error(f"Error opening icon file: {icon_file}")
                img = Image.open('icons/thermometer.png')

            # Determine Big Temp position
            current_temp = f"{temp:.0f}°F"
            temp_width, temp_height = get_size(big_number, current_temp)

            position = x_position + temp_width, y_position + 5
            icon_width, icon_height = img.size
            out.logger.debug(f"Position: {position}, {icon}")
            canvas.paste(img, position)

            ### BIG TEMP ###
            position = x_position, y_position

            out.logger.debug(f"Y position: {y_position}: {current_temp}")

            draw.text(position, f"{current_temp}", color, big_number, stroke_width=2, stroke_fill='black')

            feels_like_x_position = x_position
            temp_x_position = x_position + temp_width - 15

            y_position += big_number_height

            ### HIGH/LOW TEMP ###
            section_font = header_two

            daily_max_int = type_int(weather_data.daily[0].temp.max)
            daily_max_color, icon = temp_color(daily_max_int)
            daily_max_string = f"↑{daily_max_int:.0f}"
            daily_max_width, daily_max_height = get_size(section_font, daily_max_string)

            draw.text((x_position, y_position), daily_max_string, daily_max_color, section_font, stroke_width=1, stroke_fill='black')
            x_position += daily_max_width

            separator = " / "
            separator_width, separator_height = get_size(section_font, separator)
            draw.text((x_position, y_position), separator, 'black', section_font)
            x_position += separator_width

            daily_min_int = type_int(weather_data.daily[0].temp.min)
            daily_min_color, icon = temp_color(daily_min_int)
            daily_min_string = f"↓{daily_min_int:.0f}°F"

            draw.text((x_position, y_position), daily_min_string, daily_min_color, section_font, stroke_width=1, stroke_fill='black')

            out.logger.debug(f"Y position: {y_position}: {daily_max_string}{daily_min_string}")

            y_position += header_two_height

            ### FEELS LIKE ###
            x_position = feels_like_x_position
            daily_feels_int = type_int(weather_data.current.feels_like)
            color, unused_icon = temp_color(daily_feels_int)
            daily_feels_string = f"{daily_feels_int:.0f}°F"
            position = x_position, y_position
            out.logger.debug(f"Y position: {y_position}: Feels like: {daily_feels_string}")

            text = "Feels like: "
            text_width, text_height = get_size(paragraph, text)
            draw.text((position), text, 'black', paragraph)

            temp_position = x_position + text_width, y_position
            draw.text((temp_position), daily_feels_string, color, paragraph, stroke_width=1, stroke_fill='black')
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
                y_position = max_height / 2 + 35

                counter = 0
                for day in weather_data.daily: # Draw the header
                    counter += 1
                    if counter == 1:
                        continue # Skip the first day
                    x_position += int(max_width / 7)
                    date = time.strftime('%a %d', time.localtime(day.dt))
                    draw.text((x_position, y_position), f"{date}", 'red', forecast_header)

                y_position += forecast_header_height + 5
            else:
                y_position = max_height / 2 + 160

            city_name_trunc = city_name[:3]
            x_position = 5
            row = y_position
            y_spacing = 5

            column_width = int(max_width / 7)

            counter = 0
            for day in weather_data.daily:
                y_position = row

                counter += 1
                if counter == 1:
                    continue
                if counter == 2:
                    draw.text((x_position, y_position), f"{city_name_trunc}", 'red', forecast_city, stroke_width=1, stroke_fill='black')

                x_position += column_width

                date = time.strftime('%a %d', time.localtime(day.dt))
                pop = day.pop * 100

                max_color, icon = temp_color(day.temp.max)
                min_color, icon = temp_color(day.temp.min)

                ### MAX TEMP ###
                section_font = mid_number

                daily_max = f"{type_int(day.temp.max):.0f}"
                text = f"{daily_max}"
                draw.text((x_position, y_position), text, max_color, section_font, stroke_width=2, stroke_fill='black')
                daily_max_width, daily_max_height = get_size(section_font, text)
                temp_x_position = x_position + daily_max_width

                text = "/"
                draw.text((temp_x_position, y_position), text, 'black', section_font)
                separator_width, separator_height = get_size(section_font, text)
                temp_x_position += separator_width

                ### MIN TEMP ###
                text = f"{type_int(day.temp.min):.0f}°F"
                draw.text((temp_x_position, y_position), text, min_color, section_font, stroke_width=2, stroke_fill='black')
                dummy_width, text_height = get_size(section_font, text)

                ### WEATHER DESCRIPTION ###
                section_font = forecast_paragraph
                text = f"{day.weather.description}"
                y_position += text_height + y_spacing
                position = x_position, y_position # Use tuple since it's coded twice

                # Dynamic font size, since description can vary wildly in length
                overide_font_size = False
                temp_font_size = 14
                text_width, text_height = get_size(section_font, text)
                if text_width > column_width:
                    overide_font_size = True
                    while text_width > column_width:
                        temp_font_size -= 1
                        temp_font = ImageFont.truetype(
                            "/usr/share/fonts/truetype/Urbanist-Bold.ttf", temp_font_size)    
                        text_width, text_height = get_size(temp_font, text)

                # Used two draw commands instead of temporarily overwriting the section_font
                if overide_font_size:
                    draw.text(position, text, 'black', temp_font)
                    overide_font_size = False
                else:
                    draw.text(position, text, 'black', section_font)

                ### POP ###
                text = f"{type_int(pop)}% precip."
                y_position += text_height + y_spacing
                draw.text((x_position, y_position), text, 'black', section_font)
                text_width, text_height = get_size(section_font, text)

                ### WIND SPEED ###
                text = f"{type_int(day.wind_speed):.0f}mph"
                y_position += text_height + y_spacing
                draw.text((x_position, y_position), text, 'black', section_font)

        ### CITY FORECAST DATA ###
        y_position = header_one_height - 35
        draw_city_data(5, city_one_name, city_one_weather, draw, y_position)

        if city_two_weather:
            draw_city_data(400, city_two_name, city_two_weather, draw, y_position, 2)

        ### ACTUAL RENDERING ###
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
