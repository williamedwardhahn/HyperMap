from psd_tools import PSDImage
from PIL import Image, ImageFilter
from flask import Flask, render_template, render_template_string, url_for
app = Flask(__name__)


# ~ <meta http-equiv="refresh" content="100">

html_code = '''
<html>
<head>
    <title>Hahn</title>
</head>
<body>
<img src="{{url_for('static', filename='map.gif')}}" alt="map_data" usemap="#workmap">
<map name="workmap">
  <area shape="rect" coords="{{coords0}}" alt="{{alt0}}" href="{{path0}}">
</map>

</body>
</html>
'''


global state1

state1 = "Off" 

psd = PSDImage.open('light_bulb.psd')
group_names = [group.name for group in psd]

group = group_names.index("Light")
   
names      = [layer.name         for layer in psd[group]]
locations  = [layer.bbox         for layer in psd[group]]
images     = [layer.composite()  for layer in psd[group]] 
background = images[names.index("Background")]



@app.route('/')
def image():
	
	global state1
	
	if state1 == "Off": 
		state1 = "On"
	else:  
		state1 = "Off"

	light1      =  images[names.index(state1)]
	xy1         =  locations[names.index(state1)]
	back = background.copy()
	back.paste(light1, xy1[0:2])
	back.save('static/map.gif')
	
	
	 
	return render_template_string(html_code,coords0=xy1,alt0="text",path0="/")



app.run(port=4000)








