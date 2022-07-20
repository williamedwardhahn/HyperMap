import base64
import io
from io import BytesIO
import numpy as np
from flask import Flask
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

app = Flask(__name__)


@app.route("/")
def hello():

    points = 10

    data = np.random.rand(points, 2)

    fig = Figure()
    FigureCanvas(fig)

    ax = fig.add_subplot(111)

    ax.scatter(data[:,0], data[:,1])

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_title(f'There are {points} data points!')
    ax.grid(True)

    img = io.StringIO()
    fig.savefig(img, format='svg')
    #clip off the xml headers from the image
    svg_img = '<svg' + img.getvalue().split('<svg')[1]
    
    return svg_img
    
    
app.run(host="0.0.0.0",port=5000,debug = True)
