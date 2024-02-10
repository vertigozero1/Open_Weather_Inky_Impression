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

    header_one = ImageFont.truetype("/usr/share/fonts/truetype/Urbanist-ExtraBold.ttf", 40, encoding="unic")
    header_two = ImageFont.truetype("/usr/share/fonts/truetype/Urbanist-SemiBoldItalic.ttf", 35, encoding="unic")
    paragraph = ImageFont.truetype("/usr/share/fonts/truetype/Urbanist-Regular.ttf", 20, encoding="unic")
    big_number = ImageFont.truetype("/usr/share/fonts/truetype/Urbanist-Black.ttf", 60, encoding="unic")

    max_width = 800
    max_height = 480
    canvas = Image.new('RGB', (max_width, max_height), "white")
    draw = ImageDraw.Draw(canvas)
    
    date = time.strftime("%B %-d", time.localtime())
    weekday = time.strftime("%a", time.localtime())
    load_time = time.strftime("%-I:%M %p", time.localtime())

    def draw_city_data(x_position, city_name, weather_data, draw, header_one, paragraph, y_position):
        """ Draw the city name and weather data """
        draw.text((x_position, y_position), f"{city_name}", 'orange', header_one)
        y_position += header_one.getsize(city_name)[1] + 5

        dummy_width, paragraph_height = paragraph.getsize("A")
        draw.text((x_position, y_position), f"{weather_data.summary}", 'green', paragraph)
        draw.text((x_position, y_position + paragraph_height), f"{weather_data.weather}", 'purple', paragraph)
        
        dummy_width, big_number_height = big_number.getsize("A")
        if weather_data.temp < 50:
            color = 'blue'
        elif weather_data.temp > 80:
            color = 'red'
        else:
            color = 'black'
        draw.text((x_position, y_position + paragraph_height), f"{weather_data.temp}°F", color, big_number)
        draw.text((x_position, y_position + big_number_height), f"Feels like: {weather_data.feels_like}°F", 'black', paragraph)
        draw.text((x_position, y_position + paragraph_height), f"Humidity: {weather_data.humidity}%", 'black', paragraph)

        def get_compass_direction(degrees):
            directions = ['N', 'NNE', 'NE', 'ENE', 'E', 'ESE', 'SE', 'SSE', 'S', 'SSW', 'SW', 'WSW', 'W', 'WNW', 'NW', 'NNW']
            index = round(degrees / 22.5) % 16
            return directions[index]
        draw.text((x_position, y_position + paragraph_height), f"Wind Speed: {weather_data.daily[0].wind_speed}mph {get_compass_direction(weather_data.daily[0].wind_deg)}", 'black', paragraph)
        

    header_one = ImageFont.truetype("/usr/share/fonts/truetype/Urbanist-ExtraBold.ttf", 40, encoding="unic")
    paragraph = ImageFont.truetype("/usr/share/fonts/truetype/Urbanist-Regular.ttf", 20, encoding="unic")

    max_width = 800
    max_height = 480
    canvas = Image.new('RGB', (max_width, max_height), "white")
    draw = ImageDraw.Draw(canvas)

    date = time.strftime("%B %-d", time.localtime())
    weekday = time.strftime("%a", time.localtime())
    load_time = time.strftime("%-I:%M %p", time.localtime())

    ### Draw the [day of the week], [month] [day] header, top-left
    date_stamp = f"{weekday}, {date}"
    date_stamp_width, header_one_height = header_one.getsize(date_stamp)
    draw.text((5, 1), date_stamp, 'red', header_one)

    ### Draw the [time] header, top-right, right-justified
    time_stamp = f"Weather at {load_time}"
    time_stamp_width, header_two_height = header_one.getsize(time_stamp)
    draw.text((max_width - time_stamp_width - 5, 1), time_stamp, 'blue', header_one)

    ### Draw the city one name and establish the initial y position for the remaining text
    y_position = 1 + header_one_height + 5
    y_position_two = y_position
    draw_city_data(5, city_one_name, city_one_weather, draw, header_one, paragraph, y_position)

    if city_two_weather:
        draw.text((400, 60), f"{city_two_name}", 'orange', header_one)
        draw_city_data(400, city_two_name, city_two_weather, draw, header_one, paragraph, y_position_two)

    # save the blank canvas to a file
    canvas.save("pil-text.png", "PNG")

    inky = auto(ask_user=True, verbose=True)
    saturation = 0.5

    image = Image.open("pil-text.png")
    resizedimage = image.resize(inky.resolution)

    inky.set_image(resizedimage, saturation=saturation)
    canvas.show()
    inky.show()

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
