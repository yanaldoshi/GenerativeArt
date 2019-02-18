import os
import sys
import cv2
#import argparse

def videoToFrame(video_dir):
	for video_directory in sorted(os.listdir(video_dir)):
		_dir = os.path.join(video_dir, video_directory)
		if not os.path.isdir(_dir):
			continue
		os.chdir(_dir)
		file_names = os.listdir(_dir)
		count=1
		for video in file_names:
			if video.endswith('.mp4') or video.endswith('.gif'):
				try:
					os.mkdir(os.path.join(_dir,str(count)))
				except:
					pass
				save_dir=os.path.join(_dir, str(count))
				vidcap = cv2.VideoCapture(video)
				result, img = vidcap.read()
				i = 1
				while result:
					os.chdir(save_dir)
					cv2.imwrite("frame{:04d}.jpg".format(i),img)
					result,img=vidcap.read()
					i = i + 1
				os.chdir('..')
			count = count+1

if __name__ == '__main__':
	#parser = argparse.ArgumentParser()
	#parser.add_argument('--parent_dir', type='str', default='E:\\Programs\\Hockey_Fight_Dataset', help='parent directory')
	#args = parser.parse_args()
	videoToFrame('C:\\Users\\Smit Gangurde\\Desktop\\l33t\\Garuda\\lol\\')




