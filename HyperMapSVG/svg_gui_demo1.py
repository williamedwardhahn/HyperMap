from flask import Flask, render_template, render_template_string, url_for
app = Flask(__name__)

# ~ <meta http-equiv="refresh" content="100">

html_code = '''
<html>
<svg width="800" height="600" xmlns="http://www.w3.org/2000/svg">
 <g id="Layer_1">
  <a href="/works">
  <rect id="svg_1" visibility="{{visible1}}" height="133" width="133" y="56" x="91.5" stroke="#000" fill="#306856"  <desc>    </desc> />
  </a>
 </g>
</svg>
</html>
'''


@app.route('/')
def image():

	return render_template_string(html_code,visible1="visible") # "hidden"



@app.route("/<name>")
def hello(name):

    exec(open("./"+name+".py").read())

    return render_template_string(html_code,visible1="hidden") # "hidden"
    # return f"Ran, {name}!"



app.run(host="0.0.0.0",port=5000,debug = True)
