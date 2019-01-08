import cv2
from PIL import Image
import numpy as np
import sys
import time
import matplotlib.pyplot as plt
from threading import Thread
global pre_frame


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



def save_images(image_list):  
    index = 1   
    for image in image_list:  
        image.save(str(index) + '.png', 'PNG')
        index += 1 


def det():
	camera = cv2.VideoCapture(0)
	while(1):
		ret, frame = camera.read()
		    # 读取视频流
		    # gray_pic = img.convert('L')
		    # PIL.Image convert to np.array
		if not ret:
			print("打开摄像头失败3")
		cv2.imwrite('frame.jpg', frame)
	# np.array convert to PIL.Image
	# img = Image.fromarray(frame)
		frame = Image.open('frame.jpg')
		image_list = cut_image(frame,3)
		frame = image_list[4]
		frame = np.array(frame)
		gray_pic = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		gray_pic = cv2.resize(gray_pic, (480, 480))
		gray_pic = cv2.GaussianBlur(gray_pic, (21, 21), 0)
		global pre_frame
		if pre_frame is None:
		    pre_frame = gray_pic
		else:
			# absdiff把两幅图的差的绝对值输出到另一幅图上面来
			img_delta = cv2.absdiff(pre_frame, gray_pic)
			# threshold阈值函数(原图像应该是灰度图,对像素值进行分类的阈值,当像素值高于（有时是小于）阈值时应该被赋予的新的像素值,阈值方法)
			thresh = cv2.threshold(img_delta, 30, 255, cv2.THRESH_BINARY)[1]
			# 用一下膨胀
			thresh = cv2.dilate(thresh, None, iterations=2)
			# findContours检测物体轮廓(寻找轮廓的图像,轮廓的检索模式,轮廓的近似办法)
			image, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
			for c in contours:
				# 设置敏感度
				# contourArea计算轮廓面积
				if cv2.contourArea(c) < 1000:
				    continue
				else:
					p=cv2.imread('2.jpg')
					plt.imshow(p)
					plt.axis('off')
					plt.pause(0.5)
					plt.close()
					print(time.strftime("%H:%M:%S",time.localtime(time.time())))
					print("探测到物体！！！")
					# 保存图像
					TI = time.strftime('%Y-%m-%d', time.localtime(time.time()))
					# cv2.imwrite("D:\\python\\first_j\\" + "JC"+TI+ '.jpg', frame)
					break
		time.sleep(1)

def main():
	camera = cv2.VideoCapture(0)
	# 测试用,查看视频size
	width  = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
	height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
	size = width,height
	#打印一下分辨率
	print(repr(size))
	ret, frame = camera.read()
	if not ret:
		print("打开摄像头失败1")
	cv2.imwrite('1.jpg', frame)
    # np.array convert to PIL.Image
    # img = Image.fromarray(frame)
	img = Image.open('1.jpg')
    #image.show()  
	image_list = cut_image(img,3)
	img = image_list[4]
	img = np.array(img)
	gray_pic = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	gray_pic = cv2.resize(gray_pic, (480, 480))
	gray_pic = cv2.GaussianBlur(gray_pic, (21, 21), 0)
	global pre_frame 
	pre_frame = gray_pic
	while (1):
		ret, frame = camera.read()
	    # 读取视频流
		if not ret:
			print("打开摄像头失败2")
			break
		cv2.imshow("capture", frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
	camera.release()
	cv2.destroyAllWindows()




if __name__ == '__main__':
	main()
	thread = Thread(target = det)
	thread.start()
