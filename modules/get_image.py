import imgkit                               # for html to image conversion
from html2image import Html2Image           # alternate for html to image conversion
import traceback                            # for error handling
import sys                                  # for error handling
import time                                 # for time formatting   
from inky.auto import auto                  # for working with the e-ink display
from PIL import Image,ImageDraw,ImageFont   # for rendering via PIL
        
def render_imgkit(out):
    """ Render HTML to image using imgkit """
    try:
        imgkit.from_file('weather.html', 'weather.jpg')
    except Exception:
        out.logger.critical("Error rendering HTML to image")
        out.logger.critical(traceback.format_exc())
        sys.exit

def render_html2image(html, out):
    """ Render HTML to image using html2image """
    try:
        hti = Html2Image()
        hti.screenshot(html_str=html, save_as='weather.png')
    except Exception:
        out.logger.critical("Error rendering HTML to image")
        out.logger.critical(traceback.format_exc())
        sys.exit

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
    
    max_width = 800
    max_height = 480
    canvas = Image.new('RGB', (max_width, max_height), "white")
    draw = ImageDraw.Draw(canvas)
    
    date = time.strftime("%B %-d", time.localtime())
    weekday = time.strftime("%a", time.localtime())
    load_time = time.strftime("%-I:%M %p", time.localtime())

    header_one = ImageFont.truetype("/usr/share/fonts/truetype/Urbanist-ExtraBold.ttf", 60, encoding="unic")
    header_two = ImageFont.truetype("/usr/share/fonts/truetype/Urbanist-SemiBoldItalic.ttf", 35, encoding="unic")
    paragraph = ImageFont.truetype("/usr/share/fonts/truetype/Urbanist-Regular.ttf", 20, encoding="unic")
    big_number = ImageFont.truetype("/usr/share/fonts/truetype/Urbanist-Black.ttf", 60, encoding="unic")

    dummy_width, big_number_height = big_number.getsize("Ag") # Use 'Ag' to cover normal full range above and below the line
    dummy_width, header_one_height = header_one.getsize("Ag")
    dummy_width, header_two_height = header_two.getsize("Ag")
    time_stamp = f"Weather at {load_time}"
    time_stamp_width, paragraph_height = paragraph.getsize(time_stamp) # Use an actual string to determine the x position for right-justification on the canvas

    ### Draw the [day of the week], [month] [day] header, top-left
    date_stamp = f"{weekday}, {date}".upper()
    draw.text((5, 1), date_stamp, 'blue', header_one)

    ### Draw the [time] header, top-right, right-justified
    draw.text((max_width - time_stamp_width - 5, 1), time_stamp, 'blue', paragraph)

    def draw_city_data(x_position, city_name, weather_data, draw, y_position):
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
        icon_file = f"\icons\Freecns 2.0\PNG\Color\64\{weather_data.daily[0].icon}.png"
        
        img = Image.open(icon_file)
        icon_width, icon_height = img.size
        x_position = 400 - icon_width
        
        canvas.paste(img, (x_position, y_position))
        
        ### BIG TEMP ###
        if weather_data.current.temp < 50:
            color = 'blue'
        elif weather_data.current.temp > 80:
            color = 'red'
        else:
            color = 'black'

        out.logger.debug(f"Y position: {y_position}: {weather_data.current.temp}°F")
        draw.text((x_position, y_position), f"{weather_data.current.temp}°F", color, big_number)
        y_position += big_number_height -25

        ### HIGH/LOW TEMP ###
        out.logger.debug(f"Y position: {y_position}: {weather_data.daily[0].temp.max} / {weather_data.daily[0].temp.min}°F")
        draw.text((x_position, y_position), f"↑{weather_data.daily[0].temp.max} / ↓{weather_data.daily[0].temp.min}°F", color, header_two)
        y_position += header_two_height - 10

        ### FEELS LIKE ###
        out.logger.debug(f"Y position: {y_position}: Feels like: {weather_data.current.feels_like}°F")  
        draw.text((x_position, y_position), f"Feels like: {weather_data.current.feels_like}°F", 'black', paragraph)
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
        out.logger.debug(f"Y position: {y_position}: Wind Speed: {weather_data.daily[0].wind_speed}mph {weather_data.daily[0].wind_deg}°")
        draw.text((x_position, y_position), f"Wind Speed: {weather_data.daily[0].wind_speed}mph {get_compass_direction(weather_data.daily[0].wind_deg)}", 'black', paragraph)

    ### Draw the city one name and establish the initial y position for the remaining text
    y_position = header_one_height - 25
    draw_city_data(5, city_one_name, city_one_weather, draw, y_position)

    if city_two_weather:
        draw_city_data(400, city_two_name, city_two_weather, draw, y_position)

    # save the blank canvas to a file
    canvas.save("pil-text.png", "PNG")

    inky = auto(ask_user=True, verbose=True)
    saturation = 0.5

    image = Image.open("pil-text.png")
    resizedimage = image.resize(inky.resolution)

    inky.set_image(resizedimage, saturation=saturation)
    canvas.show()
    inky.show()

def image_example():
    """ HTML2IMG REQUIRES CHROME TO BE INSTALLED ON THE SYSTEM
    MAY REQUIRE X SERVER ON HEADLESS LINUX """
    
    hti = Html2Image()

    html = '<h1> A title </h1> Some text.'
    css = 'body {background: red;}'
    # screenshot an HTML string (css is optional)
    hti.screenshot(html_str=html, css_str=css, save_as='page.png')

    # screenshot an HTML file
    hti.screenshot(html_file='page.html',
                   css_file='style.css',
                   save_as='page2.png')

    # screenshot an URL
    hti.screenshot(url='https://www.python.org',
                   save_as='python_org.png')

    """ IMGKIT REQUIRES IMGKIT AND WKHTMLTOPDF TO BE INSTALLED ON THE SYSTEM """

    imgkit.from_url('http://google.com', 'out.jpg')
    imgkit.from_string('Hello!', 'out.jpg')
    imgkit.from_file('test.html', 'out.jpg')