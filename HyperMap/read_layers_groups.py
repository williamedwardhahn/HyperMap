from psd_tools import PSDImage
from psd_tools.constants import Tag



psd = PSDImage.open('light_bulb.psd')
group_names = [group.name for group in psd]


group = group_names.index("Light")
   
names      = [layer.name         for layer in psd[group]]
locations  = [layer.bbox         for layer in psd[group]]
images     = [layer.composite()  for layer in psd[group]] 

sizes = [layer.size  for layer in psd[group]]
# ~ print(sizes)


# ~ print(names)
# ~ print(len(psd))
# ~ print(psd[0].name)

# ~ print(names.index("On"))

# ~ images[names.index("Off")].show()

# ~ for group in psd:
	
	# ~ print(group.name)
	
	# ~ names  = [layer.name for layer in group]
	# ~ print(names)
