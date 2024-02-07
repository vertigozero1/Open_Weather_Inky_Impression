""" HTML2IMG REQUIRES CHROME TO BE INSTALLED ON THE SYSTEM
    MAY REQUIRE X SERVER ON HEADLESS LINUX """


from html2image import Html2Image
hti = Html2Image()

html = '<h1> A title </h1> Some text.'
css = 'body {background: red;}'

# screenshot an HTML string (css is optional)
hti.screenshot(html_str=html, css_str=css, save_as='page.png')


"""# screenshot an HTML file
hti.screenshot(
    html_file='page.html', css_file='style.css', save_as='page2.png'
)"""

# screenshot an URL
hti.screenshot(url='https://www.python.org', save_as='python_org.png')




""" IMGKIT REQUIRES IMGKIT AND WKHTMLTOPDF TO BE INSTALLED ON THE SYSTEM """

"""import imgkit
imgkit.from_url('http://google.com', 'out.jpg')
"""
