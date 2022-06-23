from PIL import Image, ImageFilter

status = [1,0,1]
 
base = Image.open("back.png")
on   = Image.open("on.png").convert("RGBA")   
off  = Image.open("off.png").convert("RGBA")
 
for i in range(len(status)):
	if status[i] == 1:
		light = on
	else:
		light = off
		
	base.paste(light, (20, 50+i*50))
			

base.show()
