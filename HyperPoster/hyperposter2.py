import base64
import io
from io import BytesIO
import numpy as np
from flask import Flask, render_template, render_template_string, url_for
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
app = Flask(__name__)



html_code = '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<link rel="stylesheet" href="{{ url_for('static', filename='styles/poster.css') }}">
<meta name="viewport" content="height=device-height, width=device-width, initial-scale=1">
<script type="text/javascript" id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<link href="https://fonts.googleapis.com/css2?family=Fira+Sans+Condensed:ital,wght@0,400;0,500;0,600;0,700;1,400;1,500;1,600;1,700&amp;family=Ubuntu+Mono:ital,wght@0,400;0,700;1,400;1,700&amp;display=swap" rel="stylesheet">
<style type="text/css">html { font-size: 1.15rem }</style>

<title>A Living Poster</title>

</head>

<body>
	
<header>

	<aside>
	<a href="https://mpcrlab.com"><img src="https://avatars.githubusercontent.com/u/11051475?s=280&v=4" alt="Tutorial logo"></a>
	</aside>

	<div>
	<h1>Matrix Models: MNIST</h1>
	<h2>Machine Perception and Cognitive Robotics Laboratory</h2>

	<address>
	<a>William Edward Hahn<sup>a</sup></a><br/><sup>a</sup>
	<a>FAU MPCR Lab</a>
	</address>
	</div>

	<aside>
	<a href=""><img src="" alt=""></a>
	</aside>

</header>

<main>
	
	
	<article>
	<header><h3>Abstract</h3></header>
	<p>Poster text here</p>
	</article>



	<article>
	<header><h3>Mathematics</h3></header>
	\( y = mx+b \) 
	\[ \int_0^\infty x \ dx \]
	
	</article>
	
	
	
	<article>
	<header><h3>Figure</h3></header>

	<figure>
	<img src={{image1}}>
	<figcaption>Matplotlib Plot of \( y =mx+b \) </figcaption>
	</figure>

	</article>
	


</main>


<footer>
<address>Rubin Gruber AI Sandbox</address>
<address>mpcrlab.com</address>
Florida Atlantic University 2022</a>
</footer>
</body>
</html>
'''






@app.route("/")
@app.route("/<points>")
def hello(points = "10"):

    points = int(points)

    data = np.random.rand(points, 2)

    fig = Figure()
    FigureCanvas(fig)

    ax = fig.add_subplot(111)

    ax.scatter(data[:,0], data[:,1])

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(f'There are {points} data points!')
    ax.grid(True)
    
    
    buf = BytesIO()
    fig.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    img = f"data:image/png;base64,{data}"
    
    return render_template_string(html_code, image1=img)
    
    
app.run(host="0.0.0.0",port=5000,debug = True)
