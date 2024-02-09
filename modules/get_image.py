import imgkit                       # for html to image conversion
from html2image import Html2Image   # alternate for html to image conversion
import traceback                    # for error handling
import sys                          # for error handling
from PIL import Image
from inky.auto import auto
from PIL import Image,ImageDraw,ImageFont

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


def render_pil(city1, data, out, city2 = None, data2 = None):
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
    header_one = ImageFont.truetype("/usr/share/fonts/truetype/Urbanist-Black.ttf", 40, encoding="unic")
    header_two = ImageFont.truetype("/usr/share/fonts/truetype/Urbanist-SemiBoldItalic.ttf", 35, encoding="unic")
    paragraph = ImageFont.truetype("/usr/share/fonts/truetype/Urbanist-Regular.ttf", 20, encoding="unic")

    canvas = Image.new('RGB', (800, 480), "white")
    draw = ImageDraw.Draw(canvas)
    
    draw.text((5, 1), f"{weekday}, {date}", 'red', header_one)
    draw.text((5, 30), f"Weather at {load_time}", 'blue', header_two)
    draw.text((5, 60), f"{weather_one.name}", 'orange', header_one)
    draw.text((5, 90), f"{weather_one.summary}", 'green', paragraph)
    draw.text((5, 120), f"{weather_one.weather}", 'purple', paragraph)
    draw.text((5, 150), f"Temp: {weather_one.temp}°F", 'black', paragraph)
    draw.text((5, 180), f"Feels like: {weather_one.feels_like}°F", 'black', paragraph)
    draw.text((5, 210), f"Humidity: {weather_one.humidity}%", 'black', paragraph)
    draw.text((5, 240), f"Wind: {weather_one.wind_speed} mph", 'black', paragraph)
    draw.text((5, 270), f"Wind direction: {weather_one.wind_direction}°", 'black', paragraph)
    draw.text((5, 300), f"Sunrise: {weather_one.sunrise}", 'black', paragraph)
    draw.text((5, 330), f"Sunset: {weather_one.sunset}", 'black', paragraph)

    if data2:
        draw.text((400, 60), "{weather_two.name}", 'orange', header_one)
        draw.text((400, 90), "{weather_two.summary}", 'green', paragraph)
        draw.text((400, 120), "{weather_two.weather}", 'purple', paragraph)
        draw.text((400, 150), "Temp: {weather_two.temp}°F", 'black', paragraph)
        draw.text((400, 180), "Feels like: {weather_two.feels_like}°F", 'black', paragraph)
        draw.text((400, 210), "Humidity: {weather_two.humidity}%", 'black', paragraph)
        draw.text((400, 240), "Wind: {weather_two.wind_speed} mph", 'black', paragraph)
        draw.text((400, 270), "Wind direction: {weather_two.wind_direction}°", 'black', paragraph)
        draw.text((400, 300), "Sunrise: {weather_two.sunrise}", 'black', paragraph)
        draw.text((400, 330), "Sunset: {weather_two.sunset}", 'black', paragraph)

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
