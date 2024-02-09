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

    header_one = ImageFont.truetype("/usr/share/fonts/truetype/Urbanist-Black.ttf", 40, encoding="unic")
    header_two = ImageFont.truetype("/usr/share/fonts/truetype/Urbanist-SemiBoldItalic.ttf", 35, encoding="unic")
    paragraph = ImageFont.truetype("/usr/share/fonts/truetype/Urbanist-Regular.ttf", 20, encoding="unic")

    canvas = Image.new('RGB', (800, 480), "white")
    draw = ImageDraw.Draw(canvas)
    
    date = time.strftime("%B %-d", time.localtime())
    weekday = time.strftime("%a", time.localtime())
    load_time = time.strftime("%-I:%M %p", time.localtime())

    draw.text((5, 1), f"{weekday}, {date}", 'red', header_one)
    draw.text((5, 30), f"Weather at {load_time}", 'blue', header_two)
    draw.text((5, 60), f"{city_one_name}", 'orange', header_one)
    draw.text((5, 90), f"{city_one_weather.get('summary')}", 'green', paragraph)
    draw.text((5, 120), f"{city_one_weather.get('weather')}", 'purple', paragraph)
    draw.text((5, 150), f"Temp: {city_one_weather.get('temp')}°F", 'black', paragraph)
    draw.text((5, 180), f"Feels like: {city_one_weather.get('feels_like')}°F", 'black', paragraph)
    draw.text((5, 210), f"Humidity: {city_one_weather.get('humidity')}%", 'black', paragraph)
    draw.text((5, 240), f"Wind: {city_one_weather.get('wind_speed')} mph", 'black', paragraph)
    draw.text((5, 270), f"Wind direction: {city_one_weather.get('wind_direction')}°", 'black', paragraph)

    if city_two_weather:
        draw.text((400, 60), f"{city_two_name}", 'orange', header_one)
        draw.text((400, 90), f"{city_two_weather.get('summary')}", 'green', paragraph)
        draw.text((400, 120), f"{city_two_weather.get('weather')}", 'purple', paragraph)
        draw.text((400, 150), f"Temp: {city_two_weather.get('temp')}°F", 'black', paragraph)
        draw.text((400, 180), f"Feels like: {city_two_weather.get('feels_like')}°F", 'black', paragraph)
        draw.text((400, 210), f"Humidity: {city_two_weather.get('humidity')}%", 'black', paragraph)
        draw.text((400, 240), f"Wind: {city_two_weather.get('wind_speed')} mph", 'black', paragraph)
        draw.text((400, 270), f"Wind direction: {city_two_weather.get('wind_direction')}°",'black', paragraph)

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
