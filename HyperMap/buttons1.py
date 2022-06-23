from PIL import Image, ImageFilter
from flask import Flask, render_template, url_for
app = Flask(__name__)


status = [1,1,0]
 
base = Image.open("back.png")
on   = Image.open("on.png").convert("RGBA")
off  = Image.open("off.png").convert("RGBA")
 
base.paste(on,  (20, 50))

base.paste(on,  (20, 100))

base.paste(off, (20, 150))

base.show()
