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
    
names     = [layer.name         for layer in psd]
locations = [layer.bbox         for layer in psd]
images    = [layer.composite()  for layer in psd] 

Background = images[names.index("Background")]
On         = images[names.index("On")]
Off        = images[names.index("Off")]

        
if state:
	Light = On
else:
	Light = Off    


 

Background.paste(Light, (20, 20))
Background.show()

Background.save('static/map.gif')









@app.route('/')
def image(): 
    return render_template_string(html_code,coords1="0,0,20,20")


# ~ app.run()








