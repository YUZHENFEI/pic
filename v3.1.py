import cv2
from PIL import Image
import numpy as np
import sys
import time
import matplotlib.pyplot as plt
from threading import Thread


def cut_image(image,d):
    width, height = image.size
    item_width = int(width / d)
    item_height = int(height / d)
    box_list = []
    # (left, upper, right, lower)
    for i in range(0,3):
        for j in range(0,3):
            #print((i*item_width,j*item_width,(i+1)*item_width,(j+1)*item_width))
            box = (j*item_width,i*item_height,(j+1)*item_width,(i+1)*item_height)
            box_list.append(box)
    image_list = [image.crop(box) for box in box_list]
    return image_list


def show():
	global off
	while(1):
		ret,frame = camera.read()
		cv2.imshow('Video',frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			off = 1
			break
	camera.release()
	cv2.destroyAllWindows()


def det():
	global isDetected
	global off
	img = Image.open('1.jpg')
    #image.show()  
	image_list = cut_image(img,3)
	img = image_list[4]
	img = np.array(img)
	gray_pic = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	gray_pic = cv2.resize(gray_pic, (480, 480))
	gray_pic = cv2.GaussianBlur(gray_pic, (21, 21), 0)
	pre_frame = gray_pic
	print('--初始化完成')
	print('--Q键退出')
	while (1):
		ret, frame = camera.read()
	    # 读取视频流
		if not ret:
			print("--打开摄像头失败2")
			break
		cv2.imwrite('2.jpg', frame)
		img = Image.open('2.jpg')
	    #image.show()  
		image_list = cut_image(img,3)
		img = image_list[4]
		img = np.array(img)
		gray_pic = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
		gray_pic = cv2.resize(gray_pic, (480, 480))
		gray_pic = cv2.GaussianBlur(gray_pic, (21, 21), 0)

		img_delta = cv2.absdiff(pre_frame, gray_pic)
		# threshold阈值函数(原图像应该是灰度图,对像素值进行分类的阈值,当像素值高于（有时是小于）阈值时应该被赋予的新的像素值,阈值方法)
		thresh = cv2.threshold(img_delta, 180, 255, cv2.THRESH_BINARY)[1]
		# 用一下膨胀
		thresh = cv2.dilate(thresh, None, iterations=2)
		# findContours检测物体轮廓(寻找轮廓的图像,轮廓的检索模式,轮廓的近似办法)
		image, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
		for c in contours:
			if cv2.contourArea(c) < 1000:
				    continue
			else:
				isDetected = 1
				break
		if off == 1:
			break



if __name__ == '__main__':
	print('-------9宫探测脚本-------')
	print('--正在初始化...')
	isDetected = 0
	off = 0
	camera = cv2.VideoCapture(0)
	# 测试用,查看视频size
	width  = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
	height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
	size = width,height
	#打印一下分辨率
	print('--分辨率：',repr(size))
    # np.array convert to PIL.Image
    # img = Image.fromarray(frame)
	ret, frame = camera.read()
	cv2.imwrite('1.jpg', frame)
	thread1 = Thread(target=show)
	thread2 = Thread(target=det)
	thread1.start()
	thread2.start()
	while(1):
		if(isDetected == 1):
			p=cv2.imread('p.jpg')
			plt.imshow(p)
			plt.axis('off')
			plt.pause(0.5)
			plt.close()
			print('**',end = '')
			print(time.strftime("%H:%M:%S",time.localtime(time.time())),end = '')
			print('**')
			print("--探测到物体！！！")
			isDetected = 0
		if(off == 1):
			print('--退出脚本')
			break
