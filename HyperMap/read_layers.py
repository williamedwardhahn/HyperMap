from psd_tools import PSDImage

psd = PSDImage.open('back.psd')

# ~ for layer in psd:
    # ~ print(layer.name)
    # ~ print(layer.bbox)
    # ~ layer_image = layer.composite()
    # ~ layer_image.show()
    # ~ layer_image.save('%s.png' % layer.name)
    
    
names = [layer.name for layer in psd]

print(names)

print(len(psd))
print(psd[0].name)
