import imgkit                       # for html to image conversion
from html2image import Html2Image   # alternate for html to image conversion
import traceback                    # for error handling
import sys                          # for error handling

def render_imgkit(html, out):
    """ Render HTML to image using imgkit """
    try:
        imgkit.from_string(html, 'weather.jpg')
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
