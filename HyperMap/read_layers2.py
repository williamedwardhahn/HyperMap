from psd_tools import PSDImage
from psd_tools.constants import Tag



psd = PSDImage.open('light_bulb.psd')
    
names     = [layer.name         for layer in psd]
locations = [layer.bbox         for layer in psd]
images    = [layer.composite()  for layer in psd] 

# ~ print(names)
# ~ print(len(psd))
# ~ print(psd[0].name)



# ~ print(names.index("On"))


# ~ images[names.index("Off")].show()

for layer in psd:
	metadata = layer.tagged_blocks.get_data(Tag.METADATA_SETTING)
	print(metadata)
