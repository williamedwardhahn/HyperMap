# HyperPoster
# William Edward Hahn
# MPCR Lab
# 2022

import base64
import io
from io import BytesIO
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import numpy as np
from imageio import *
from skimage.transform import resize
from mpl_toolkits.axes_grid1.axes_rgb import make_rgb_axes, RGBAxes
import matplotlib.pyplot as plt
import torch
from torchvision import datasets, models, transforms
from skimage.util import montage
import time
import threading
from flask import Flask, render_template, render_template_string, url_for, request
app = Flask(__name__)



def plot(x):
	if type(x) == torch.Tensor :
		x = x.cpu().detach().numpy()

	fig, ax = plt.subplots()
	im = ax.imshow(x, cmap = 'gray')
	ax.axis('off')
	fig.set_size_inches(5, 5)
	plt.show()

def montage_plot(x):
	x = np.pad(x, pad_width=((0, 0), (1, 1), (1, 1)), mode='constant', constant_values=0)
	plot(montage(x))


def one_hot(y):
	y2 = GPU_data(torch.zeros((y.shape[0],10)))
	for i in range(y.shape[0]):
		y2[i,int(y[i])] = 1
	return y2


# #MNIST
train_set = datasets.MNIST('./data', train=True, download=True)
test_set = datasets.MNIST('./data', train=False, download=True)

X = train_set.data.numpy()
X_test = test_set.data.numpy()
Y = train_set.targets.numpy()
Y_test = test_set.targets.numpy()

X = X[:,None,:,:]/255
X_test = X_test[:,None,:,:]/255

X = X.reshape(X.shape[0],784)
X_test = X_test.reshape(X_test.shape[0],784)


def CPU(data):
    return torch.tensor(data, requires_grad=True, dtype=torch.float, device=torch.device('cpu'))
    
def CPU_data(data):
    return torch.tensor(data, requires_grad=False, dtype=torch.float, device=torch.device('cpu'))


X = CPU_data(X)
Y = CPU_data(Y)
X_test = CPU_data(X_test)
Y_test = CPU_data(Y_test)



def softmax(x):
	s1 = torch.exp(x - torch.max(x,1)[0][:,None])
	s = s1 / s1.sum(1)[:,None]
	return s

def cross_entropy(outputs, labels):            
	return -torch.sum(softmax(outputs).log()[range(outputs.size()[0]), labels.long()])/outputs.size()[0]

def Truncated_Normal(size):

	u1 = torch.rand(size)*(1-np.exp(-2)) + np.exp(-2)
	u2 = torch.rand(size)
	z  = torch.sqrt(-2*torch.log(u1)) * torch.cos(2*np.pi*u2)

	return z

def acc(out,y):
	return (torch.sum(torch.max(out,1)[1] == y).item())/y.shape[0]

def get_batch(mode):

	if mode == "train":
		r = np.random.randint(X.shape[0]-b) 
		x = X[r:r+b,:]
		y = Y[r:r+b]
	elif mode == "test":
		r = np.random.randint(X_test.shape[0]-b)
		x = X_test[r:r+b,:]
		y = Y_test[r:r+b]
	return x,y

def model(x,w):

	return x@w[0]

def gradient_step(w):

	w[0].data = w[0].data - L*w[0].grad.data
	w[0].grad.data.zero_()



L = 0.05
b = 1024
epochs = 10000

plot_train = np.zeros((epochs,)) 
plot_test  = np.zeros((epochs,))
plt.plot(plot_test[0:epochs:10,])
plt.savefig('static/plot1.png')
plt.close()



def train():
	global training 

	w = [CPU(Truncated_Normal((784,10)))]

	optimizer = torch.optim.Adam(w, lr=L)  

	for i in range(epochs):
		
		x,y   = get_batch('train')
		xt,yt = get_batch('test')
		plot_train[i] = acc(model(x,w),y)
		plot_test[i] = acc(model(xt,w),yt)
		
		print(i,plot_test[i])
		if plot_test[i] > 0.98:
			break

		out = model(x,w)
		loss = cross_entropy(softmax(out),y)
		optimizer.zero_grad()
		loss.backward()
		optimizer.step()

		if i % 100 == 0:
			plt.plot(plot_test[0:i:10])
			plt.savefig('static/plot1.png')
			plt.close()


	training = False



html_code = '''
<!DOCTYPE html>
<html lang="en">
<head>
<meta http-equiv="refresh" content="5">
<meta charset="utf-8">
<link rel="stylesheet" href="{{ url_for('static', filename='styles/HahnPoster.css') }}">
<meta name="viewport" content="height=device-height, width=device-width, initial-scale=1">
<script type="text/javascript" id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<style type="text/css">html { font-size: 1.15rem }</style>

<title>A Living Poster</title>

</head>

<body>
	
<header>

	<aside>
	<a href="https://mpcrlab.com"><img src="https://avatars.githubusercontent.com/u/11051475?s=280&v=4" alt="Tutorial logo"></a>
	</aside>

	<div>
	<h1>Artificial Intelligent Life</h1>
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
	<img src="{{url_for('static', filename='plot1.png')}}">
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



global training

training = False

@app.route("/")
@app.route("/<points>")
def hello(points = "10"):
	global training

	if not training:
		training = True
		thread = threading.Thread(target=train)
		thread.start()


	page = render_template_string(html_code)
    
	return page
    
    
    
    
    
    
    
    
    
    
    
    
app.run(host="0.0.0.0",port=5000,debug = True)
