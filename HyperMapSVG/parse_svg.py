import xml.etree.ElementTree as ET

xml = ET.parse('lights.svg')

root = xml.getroot()

print(root.find('.//rect[@id="svg_1"]').get('style'))

root.find('.//rect[@id="svg_1"]').set('style','display:none')

xml.write('lights2.svg')




import xml.etree.ElementTree as ET

xml = ET.parse('lights20.svg')

root = xml.getroot()

print(root.find('.//rect[@id="svg_1"]'))

print(root.find('.//rect[@id="svg_1"]').get('style'))

root.find('.//rect[@id="svg_1"]').set('style','display:none')

xml.write('lights0.svg')




#parent
print(xml.findall('.//rect[@id="svg_1"]...'))
