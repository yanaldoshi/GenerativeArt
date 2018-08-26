from PIL import Image,ImageDraw
import numpy as np
import threading

src_path="loveo2o_hd.jpg"
img=Image.open(src_path)
canvas_img=Image.new("RGBA",img.size,(255,255,255))
canvas=ImageDraw.Draw(canvas_img)
frames=300
iterations=1000000
counter=iterations//frames
_counter=0
names=["bounce/frame{:04d}.gif".format(i) for i in range(frames)]
name_ind=0

speed_x=15
speed_y=15
size=15

x,y=(100,100)

def frameMaker(canvas_img,name_ind):
	frame=canvas_img.copy()
	frameDraw=ImageDraw.Draw(frame)
	frameDraw.rectangle([(x,y),(x+size,y+size)],fill=tuple(avg_color))
	frame.save(names[name_ind])

for i in range(iterations):
	x=x+speed_x
	y=y+speed_y
	if x>img.size[0]-50:
		speed_x=-speed_x
		x=img.size[0]-50
		y=y+size
	elif x<0:
		speed_x=-speed_x
		x=0
		y=y+size
	if y>img.size[1]-50:
		speed_y=-speed_y
		y=img.size[1]-50
		x=x+size
	elif y<0:
		speed_y=-speed_y
		y=0
		x=x+size
	'''box=(x,y,x+size,y+size)
	region=img.crop(box)
	reg_arr=np.array(region)
	temp_arr=np.sum(reg_arr,axis=1,dtype=np.uint8)
	temp_arr=np.sum(temp_arr,axis=0,dtype=np.uint8)
	avg_color=np.array(temp_arr/(reg_arr.shape[0]),dtype=np.uint8)'''
	src_pixels=[]
	for _x in range(x,x+size):
		for _y in range(y,y+size):
			src_pixels.append(img.getpixel((_x,_y)))
	avg_color=[0,0,0]
	for pixel in src_pixels:
		avg_color[0]=avg_color[0]+pixel[0]
		avg_color[1]=avg_color[1]+pixel[1]
		avg_color[2]=avg_color[2]+pixel[2]
	for n in range(3):
		avg_color[n]=avg_color[n]//len(src_pixels)
	canvas.rectangle([(x,y),(x+size,y+size)],fill=tuple(avg_color))
	if _counter==counter:
		threading.Thread(target=frameMaker,args=(canvas_img,name_ind)).start()
		name_ind=name_ind+1
		_counter=0
	else:
		_counter=_counter+1

images=[]

for i in range(frames):
	try:
		frame=Image.open(names[i])
		images.append(frame)
	except:
		pass
images[0].save('testing11.gif',save_all=True,append_images=images[1:],duration=1,loop=0)