from PIL import Image, ImageFilter
from flask import Flask, render_template, url_for
app = Flask(__name__)

 
img1 = Image.open("back.png")
img2 = Image.open("off.png")
 
img2 = img2.convert("RGBA")  # Including the "A" in RGB
 
img1.paste(img2, (20, 20), img2)
img1.show()

img1.save('map.gif')
