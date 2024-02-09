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


def render_pil():
    """ Render text to image using PIL """
    ''' Urbanist-Thin.ttf
            Urbanist-ThinItalic.ttf
        Urbanist-ExtraLight.ttf
            Urbanist-ExtraLightItalic.ttf
        Urbanist-Light.ttf
            Urbanist-LightItalic.ttf
        Urbanist-Regular.ttf
            Urbanist-Italic.ttf
        Urbanist-Medium.ttf
            Urbanist-MediumItalic.ttf
        Urbanist-SemiBold.ttf
            Urbanist-SemiBoldItalic.ttf
        Urbanist-Bold.ttf
            Urbanist-BoldItalic.ttf
        Urbanist-ExtraBold.ttf
            Urbanist-ExtraBoldItalic.ttf
        Urbanist-Black.ttf
            Urbanist-BlackItalic.ttf
       '''
    message_one = u"URBANIST extraBold, in blue"
    message_two = u"URBANIST lightItalic, in orange"
    
    font_one = ImageFont.truetype("/usr/share/fonts/truetype/Urbanist-ExtraBold.ttf", 10, encoding="unic")
    font_two = ImageFont.truetype("/usr/share/fonts/truetype/Urbanist-LightItalic.ttf", 10, encoding="unic")

    # get the line size
    text_width, text_height = font_one.getsize(message_one)
    text_width_two, text_height_two = font_two.getsize(message_two)

    total_width = text_width + text_width_two + 10
    total_height = text_height + text_height_two + 10

    # create a blank canvas with extra space between lines
    canvas = Image.new('RGB', (800, 480), "orange")

    # draw the text onto the text canvas, and use blue as the text color
    draw = ImageDraw.Draw(canvas)
    
    draw.text((5,1), message_one, 'blue', font_one)
    draw.text((5,10), message_two, 'orange', font_two)

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
