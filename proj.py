from PIL import Image
from PIL import ImageDraw
from random import randint
import threading


src_path="loveo2o_hd.jpg"
canvas_path="loveo2o_proj.jpg"
src_img=Image.open(src_path)
canvas_img=Image.new("RGBA",src_img.size,(255,255,255))
canvas_img2=Image.new("RGBA",src_img.size,(255,255,255))
canvas_draw=ImageDraw.Draw(canvas_img)
canvas2_draw=ImageDraw.Draw(canvas_img2)
frames=150
names=['imgs/img{:03d}.gif'.format(i) for i in range(frames)]
name_ind=0
counter=0
_counter=0
iterations=1000000
lim=iterations//frames
status_lim=iterations//10
#flag=False
'''for n in range(1,6):
	for x in range(0,src_img.size[0]-n,n):
		for y in range(0,src_img.size[1]-n,n):
			src_pixels=[]
			canvas_pixels=[]
			canvas2_pixels=[]
			for _x in range(x,x+n):
				for _y in range(y,y+n):
					src_pixels.append(src_img.getpixel((_x,_y)))
					canvas_pixels.append(canvas_img.getpixel((_x,_y)))
					canvas2_pixels.append(canvas_img2.getpixel((_x,_y)))
			src_avg=[0,0,0]
			canvas_avg=[0,0,0]
			canvas2_avg=[0,0,0]
			for pixel in src_pixels:
				src_avg[0]=src_avg[0]+pixel[0]
				src_avg[1]=src_avg[1]+pixel[1]
				src_avg[2]=src_avg[2]+pixel[2]
			src_avg[0]=src_avg[0]//len(src_pixels)
			src_avg[1]=src_avg[1]//len(src_pixels)
			src_avg[2]=src_avg[2]//len(src_pixels)
			for pixel in canvas_pixels:
				canvas_avg[0]=canvas_avg[0]+pixel[0]
				canvas_avg[1]=canvas_avg[1]+pixel[1]
				canvas_avg[2]=canvas_avg[2]+pixel[2]
			canvas_avg[0]=canvas_avg[0]//len(canvas_pixels)
			canvas_avg[1]=canvas_avg[1]//len(canvas_pixels)
			canvas_avg[2]=canvas_avg[2]//len(canvas_pixels)
			for pixel in canvas2_pixels:
				canvas2_avg[0]=canvas2_avg[0]+pixel[0]
				canvas2_avg[1]=canvas2_avg[1]+pixel[1]
				canvas2_avg[2]=canvas2_avg[2]+pixel[2]
			canvas2_avg[0]=canvas2_avg[0]//len(canvas2_pixels)
			canvas2_avg[1]=canvas2_avg[1]//len(canvas2_pixels)
			canvas2_avg[2]=canvas2_avg[2]//len(canvas2_pixels)
			canvas_diff=[0,0,0]
			canvas2_diff=[0,0,0]
			for i in range(3):
				canvas_diff[i]=abs(canvas_avg[i]-src_avg[i])
				canvas2_diff[i]=abs(canvas2_avg[i]-src_avg[i])
			if sum(canvas2_diff) >= sum(canvas_diff):
				canvas_draw.rectangle([(x,y),(x+n,y+n)],fill=(src_avg[0],src_avg[1],src_avg[2]))
				canvas2_draw.rectangle([(x,y),(x+n,y+n)],fill=(src_avg[0],src_avg[1],src_avg[2]))
			else:
				canvas_draw.rectangle([(x,y),(x+n,y+n)],fill=(canvas2_avg[0],canvas2_avg[1],canvas2_avg[2]))'''

def findAvg(pixels,avg_arr):
	for pixel in pixels:
		avg_arr[0]=avg_arr[0]+pixel[0]
		avg_arr[1]=avg_arr[1]+pixel[1]
		avg_arr[2]=avg_arr[2]+pixel[2]
	avg_arr[0]=avg_arr[0]//len(pixels)
	avg_arr[1]=avg_arr[1]//len(pixels)
	avg_arr[2]=avg_arr[2]//len(pixels)
	return avg_arr

def frameMaker(img,color):
	frame=img.copy()
	frameDraw=ImageDraw.Draw(frame)
	frameDraw.rectangle([(x,y),(x+_s,y+_s)],fill=tuple(color))
	frame.save(names[name_ind])
maxsize=15
for n in range(iterations):
	x=randint(0,src_img.size[0]-maxsize)
	y=randint(0,src_img.size[1]-maxsize)
	s=randint(1,maxsize)
	_s=randint(1,maxsize)
	src_pixels=[]
	canvas_pixels=[]
	canvas2_pixels=[]
	for _x in range(x,x+s):
		for _y in range(y,y+s):
			src_pixels.append(src_img.getpixel((_x,_y)))
			canvas_pixels.append(canvas_img.getpixel((_x,_y)))
			#canvas2_pixels.append(canvas_img2.getpixel((_x,_y)))
	for _x in range(x,x+_s):
		for _y in range(y,y+_s):
			canvas2_pixels.append(canvas_img2.getpixel((_x,_y)))

	src_avg=[0,0,0]
	canvas_avg=[0,0,0]
	canvas2_avg=[0,0,0]
	threading.Thread(target=findAvg,args=(src_pixels,src_avg)).start()
	threading.Thread(target=findAvg,args=(canvas_pixels,canvas_avg)).start()
	threading.Thread(target=findAvg,args=(canvas2_pixels,canvas2_avg)).start()

	'''src_avg=[0,0,0]
	canvas_avg=[0,0,0]
	canvas2_avg=[0,0,0]
	for pixel in src_pixels:
		src_avg[0]=src_avg[0]+pixel[0]
		src_avg[1]=src_avg[1]+pixel[1]
		src_avg[2]=src_avg[2]+pixel[2]
	src_avg[0]=src_avg[0]//len(src_pixels)
	src_avg[1]=src_avg[1]//len(src_pixels)
	src_avg[2]=src_avg[2]//len(src_pixels)
	for pixel in canvas_pixels:
		canvas_avg[0]=canvas_avg[0]+pixel[0]
		canvas_avg[1]=canvas_avg[1]+pixel[1]
		canvas_avg[2]=canvas_avg[2]+pixel[2]
	canvas_avg[0]=canvas_avg[0]//len(canvas_pixels)
	canvas_avg[1]=canvas_avg[1]//len(canvas_pixels)
	canvas_avg[2]=canvas_avg[2]//len(canvas_pixels)
	for pixel in canvas2_pixels:
		canvas2_avg[0]=canvas2_avg[0]+pixel[0]
		canvas2_avg[1]=canvas2_avg[1]+pixel[1]
		canvas2_avg[2]=canvas2_avg[2]+pixel[2]
	canvas2_avg[0]=canvas2_avg[0]//len(canvas2_pixels)
	canvas2_avg[1]=canvas2_avg[1]//len(canvas2_pixels)
	canvas2_avg[2]=canvas2_avg[2]//len(canvas2_pixels)'''
	canvas_diff=[0,0,0]
	canvas2_diff=[0,0,0]
	for i in range(3):
		canvas_diff[i]=abs(canvas_avg[i]-src_avg[i])
		canvas2_diff[i]=abs(canvas2_avg[i]-src_avg[i])
	if sum(canvas2_diff) >= sum(canvas_diff):
		#canvas_draw.rectangle([(x,y),(x+s,y+s)],fill=(src_avg[0],src_avg[1],src_avg[2]))
		'''frame=canvas_img.copy()
		frameDraw=ImageDraw.Draw(frame)
		frameDraw.rectangle([(x,y),(x+s,y+s)],fill=(src_avg[0],src_avg[1],src_avg[2]))
		frame.save(names[name_ind])
		name_ind=name_ind+1'''
		#canvas2_draw.rectangle([(x,y),(x+_s,y+_s)],fill=(src_avg[0],src_avg[1],src_avg[2]))
		canvas_draw.rectangle([(x,y),(x+_s,y+_s)],fill=(src_avg[0],src_avg[1],src_avg[2]))
		canvas2_draw.rectangle([(x,y),(x+_s,y+_s)],fill=(src_avg[0],src_avg[1],src_avg[2]))
		#flag=True
	else:
		canvas_draw.rectangle([(x,y),(x+_s,y+_s)],fill=(canvas2_avg[0],canvas2_avg[1],canvas2_avg[2]))
		#flag=False

	if counter==status_lim:
		_counter=_counter+1
		print('#')
		counter=0
	else:
		counter=counter+1
	if _counter==lim:
		threading.Thread(target=frameMaker,args=(canvas_img,canvas2_avg)).start()
		name_ind=name_ind+1
		_counter=0
	else:
		_counter=_counter+1
		'''frame=canvas_img.copy()
		frameDraw=ImageDraw.Draw(frame)
		frameDraw.rectangle([(x,y),(x+s,y+s)],fill=(src_avg[0],src_avg[1],src_avg[2]))
		frame.save(names[name_ind])
		name_ind=name_ind+1'''
images=[]
#src_img.close()
#canvas_img2.close()
for n in range(frames):
	try:
		frame=Image.open(names[n])
		images.append(frame)
	except:
		pass
images[0].save('testing10.gif',save_all=True,append_images=images[1:],duration=1,loop=0)
'''

For converting to mp4:

ffmpeg -i testing12.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" video.mp4

'''

canvas_img.show()
		




