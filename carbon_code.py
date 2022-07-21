
import urllib.request
from PIL import Image
import matplotlib.pyplot as plt

urllib.request.urlretrieve('http://127.0.0.1:5000/?code=Hello%20World&windowControls=false&language=python',"image1.png")
  
im = Image.open("image1.png")

plt.imshow(im)
plt.show()


