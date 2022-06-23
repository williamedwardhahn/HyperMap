from psd_tools import PSDImage
from PIL import Image, ImageFilter
from flask import Flask, render_template, render_template_string, url_for
app = Flask(__name__)


html_code = '''
<html>
<head>
    <title>Page Title</title>
    <meta http-equiv="refresh" content="100">
</head>

<body>

<img src="{{url_for('static', filename='map.gif')}}" alt="map_data" usemap="#workmap">

<map name="workmap">
  <area shape="rect" coords="{{coords0}}" alt="{{alt0}}" href="{{path0}}">
</map>

</body>
</html>
'''


state1 = "Off" 

psd = PSDImage.open('light_bulb.psd')
group_names = [group.name for group in psd]

group = group_names.index("Light")
   
   
names      = [layer.name         for layer in psd[group]]
locations  = [layer.bbox         for layer in psd[group]]
images     = [layer.composite()  for layer in psd[group]] 
background = images[names.index("Background")]



light1      =  images[names.index(state1)]  
xy1         =  locations[names.index(state1)]
coords1     =  str(xy1).replace("(","").replace(")","")



background.paste(light1, xy1)
background.show()

background.save('static/map.gif')









@app.route('/')
def image(): 
    return render_template_string(html_code,coords0=str(xy1),alt0="text",path0="/hello")


app.run()








