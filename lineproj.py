from PIL import Image
from PIL import ImageDraw
from random import randint
import threading

src_path="loveo2o_hd.jpg"
canvas_path="loveo2o_proj.jpg"
src_img=Image.open(src_path)
src_size=src_img.size
canvas_img=Image.new("RGBA",src_img.size,(255,255,255))
canvas_img2=Image.new("RGBA",src_img.size,(255,255,255))
canvas_draw=ImageDraw.Draw(canvas_img)
canvas2_draw=ImageDraw.Draw(canvas_img2)
frames=100
names=['imgs1/img{:03d}.gif'.format(i) for i in range(frames)]
name_ind=0
counter=0
_counter=0
flag=True
iterations=5000000
lim=iterations//frames
status_lim=iterations//10
max_linesize=17


def getLine(x,y,s):
	line_pixels=[]
	#case=randint(0,1)
	case=0
	if case==0:
		for i in range(s):
			temp_x=x+i
			temp_y=y+i

			if temp_x>=src_size[0] or temp_y>=src_size[1]:
				return line_pixels
			else:
				line_pixels.append((temp_x,temp_y))

	elif case==1:
		for i in range(s):
			temp_x=x+i
			if temp_x>=src_size[0]:
				return line_pixels
			else:
				line_pixels.append((temp_x,y))
	elif case==2:
		for i in range(s):
			temp_y=y+i
			if temp_y>=src_size[1]:
				return line_pixels
			else:
				line_pixels.append((x,temp_y))
	elif case==3:
		for i in range(s):
			temp_x=x-i
			temp_y=y+i
			if temp_y>=src_size[1] or temp_x<0:
				return line_pixels
			else:
				line_pixels.append((temp_x,temp_y))
	
	return line_pixels

def drawLine(canvas,pixels,fill_col):
	canvas.point(pixels,fill=fill_col)

def findAvg(pixels,avg_arr):
	for pixel in pixels:
		avg_arr[0]=avg_arr[0]+pixel[0]
		avg_arr[1]=avg_arr[1]+pixel[1]
		avg_arr[2]=avg_arr[2]+pixel[2]
	avg_arr[0]=avg_arr[0]//len(pixels)
	avg_arr[1]=avg_arr[1]//len(pixels)
	avg_arr[2]=avg_arr[2]//len(pixels)
	return avg_arr

def frameSaver(canvas_img,line_pixels,src_avg,canvas2_avg,name_ind):
	frame=canvas_img.copy()
	frameDraw=ImageDraw.Draw(frame)
	if flag:
		drawLine(frameDraw,line_pixels,(src_avg[0],src_avg[1],src_avg[2]))
	else:
		drawLine(frameDraw,line_pixels,(canvas2_avg[0],canvas2_avg[1],canvas2_avg[2]))
	frame.save(names[name_ind])

for n in range(iterations):
	x=randint(0,src_size[0]-max_linesize)
	y=randint(0,src_size[1]-max_linesize)
	s=randint(1,max_linesize-1)
	line_pixels=getLine(x,y,s)
	src_pixels=[]
	canvas_pixels=[]
	canvas2_pixels=[]
	for pixelpos in line_pixels:
		src_pixels.append(src_img.getpixel(pixelpos))
		canvas_pixels.append(canvas_img.getpixel(pixelpos))
		canvas2_pixels.append(canvas_img2.getpixel(pixelpos))
	src_avg=[0,0,0]
	canvas_avg=[0,0,0]
	canvas2_avg=[0,0,0]
	threading.Thread(target=findAvg,args=(src_pixels,src_avg,)).start()
	threading.Thread(target=findAvg,args=(canvas_pixels,canvas_avg,)).start()
	threading.Thread(target=findAvg,args=(canvas2_pixels,canvas2_avg,)).start()
	#src_avg=findAvg(src_pixels,src_avg)
	#canvas_avg=findAvg(src_pixels,canvas_avg)
	#canvas2_avg=findAvg(src_pixels,canvas2_avg)
	'''for pixel in src_pixels:
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
		threading.Thread(target=drawLine,args=(canvas_draw,line_pixels,(src_avg[0],src_avg[1],src_avg[2]),)).start()
		threading.Thread(target=drawLine,args=(canvas2_draw,line_pixels,(src_avg[0],src_avg[1],src_avg[2]),)).start()
		#drawLine(canvas_draw,line_pixels,(src_avg[0],src_avg[1],src_avg[2]))
		#drawLine(canvas2_draw,line_pixels,(src_avg[0],src_avg[1],src_avg[2]))
		flag=True
		#canvas_draw.line((x,y,x+s,y+s),fill=(src_avg[0],src_avg[1],src_avg[2]))
		#canvas2_draw.line((x,y,x+s,y+s),fill=(src_avg[0],src_avg[1],src_avg[2]))
	else:
		threading.Thread(target=drawLine,args=(canvas_draw,line_pixels,(canvas2_avg[0],canvas2_avg[1],canvas2_avg[2]),)).start()
		#drawLine(canvas_draw,line_pixels,(canvas2_avg[0],canvas2_avg[1],canvas2_avg[2]))
		flag=False
		#canvas_draw.line((x,y,x+s,y+s),fill=(canvas2_avg[0],canvas2_avg[1],canvas2_avg[2]))

	if counter==status_lim:
		_counter=_counter+1
		print('#')
		counter=0
	else:
		counter=counter+1
	if _counter==lim:
		threading.Thread(target=frameSaver,args=(canvas_img,line_pixels,src_avg,canvas2_avg,name_ind)).start()
		'''frame=canvas_img.copy()
		frameDraw=ImageDraw.Draw(frame)
		if flag:
			drawLine(frameDraw,line_pixels,(src_avg[0],src_avg[1],src_avg[2]))
		else:
			drawLine(frameDraw,line_pixels,(canvas2_avg[0],canvas2_avg[1],canvas2_avg[2]))
		frame.save(names[name_ind])'''
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
def frameMaker(name,images,ind):
	try:
		frame=Image.open(names[n])
		images.insert(ind,frame)
	except:
		pass

for n in range(frames):
	frameMaker(names[n],images,n)
	'''if n==frames-1:
		_t=threading.Thread(target=frameMaker,args=(names[n],images,n,))
		_t.start()
	else:
		threading.Thread(target=frameMaker,args=(names[n],images,n,)).start()
_t.join()'''
images[0].save('testing12.gif',save_all=True,append_images=images[1:],duration=1,loop=0)
'''
For converting to mp4:

ffmpeg -i testing12.gif -movflags faststart -pix_fmt yuv420p -vf "scale=trunc(iw/2)*2:trunc(ih/2)*2" video.mp4
'''

canvas_img.show()