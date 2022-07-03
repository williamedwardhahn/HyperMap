import xml.etree.ElementTree as ET


xml = ET.parse('lights.svg')
root = xml.getroot()


root.find('.//rect[@id="svg_1"]').set('style','display:none')

xml.write('lights2.svg')




