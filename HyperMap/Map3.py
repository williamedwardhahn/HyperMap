from psd_tools import PSDImage
from PIL import Image, ImageFilter
from flask import Flask, render_template, render_template_string, url_for
app = Flask(__name__)


html_code = '''
<html>
<body>

<img src="{{url_for('static', filename='map.gif')}}" alt="map_data" usemap="#workmap">

<map name="workmap">
  <area shape="rect" coords={{coords1}} alt="home" href="/home">
</map>

</body>
</html>
'''


state = 0 


psd = PSDImage.open('light_bulb.psd')



for layer in psd:
    print(layer.name)
    print(layer.bbox)
    layer_image = layer.composite()
    # ~ layer_image.show()
    # ~ layer_image.save('%s.png' % layer.name)
    
    
    


 
img1 = Image.open("back.png")
img2 = (Image.open("on.png")).convert("RGBA")
 

img1.paste(img2, (20, 20), img2)
#img1.show()

img1.save('static/map.gif')









@app.route('/')
def image(): 
    return render_template_string(html_code,coords1="0,0,20,20")


# ~ app.run()








