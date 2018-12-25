import cv2
from PIL import Image
import numpy as np
import sys
import time



#先将 input image 填充为正方形  
def fill_image(image):  
    width, height = image.size      
    #选取长和宽中较大值作为新图片的  
    new_image_length = width if width > height else height      
    #生成新图片[白底]  
    new_image = Image.new(image.mode, (new_image_length, new_image_length), color='white')   #注意这个函数！  
    #将之前的图粘贴在新图上，居中   
    if width > height:#原图宽大于高，则填充图片的竖直维度  #(x,y)二元组表示粘贴上图相对下图的起始位置,是个坐标点。  
        new_image.paste(image, (0, int((new_image_length - height) / 2)))  
    else:  
        new_image.paste(image, (int((new_image_length - width) / 2),0))      
    return new_image  


def cut_image(image):
    width, height = image.size
    item_width = int(width / 3)  
    box_list = []
    # (left, upper, right, lower)
    for i in range(0,3):
        for j in range(0,3):
            #print((i*item_width,j*item_width,(i+1)*item_width,(j+1)*item_width))
            box = (j*item_width,i*item_width,(j+1)*item_width,(i+1)*item_width)
            box_list.append(box)
    image_list = [image.crop(box) for box in box_list]
    return image_list
#保存  


def save_images(image_list):  
    index = 1   
    for image in image_list:  
        image.save(str(index) + '.png', 'PNG')  
        index += 1  



if __name__ == '__main__':  
    
	camera = cv2.VideoCapture(0)
	# 测试用,查看视频size
	width  = int(camera.get(cv2.CAP_PROP_FRAME_WIDTH))
	height = int(camera.get(cv2.CAP_PROP_FRAME_HEIGHT))
	size = width,height
	#打印一下分辨率
	print(repr(size))
	pre_frame = None
	 
	while (1):
	    # 读取视频流
	    ret, frame = camera.read()
	    cv2.imwrite('1.jpg', frame)
	    # np.array convert to PIL.Image
	    # img = Image.fromarray(frame)
	    img = Image.open('1.jpg')     
	    #image.show()  
	    img = fill_image(img)  
	    image_list = cut_image(img)
	    img = image_list[4]

	    # 转灰度图
	    # gray_pic = img.convert('L')
	    # PIL.Image convert to np.array
	    img = np.array(img)
	    gray_pic = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	 
	    if not ret:
	        print("打开摄像头失败")
	        break
	 
	    cv2.imshow("capture", frame)
	    gray_pic = cv2.resize(gray_pic, (480, 480))
	    gray_pic = cv2.GaussianBlur(gray_pic, (21, 21), 0)
	    if pre_frame is None:
	        pre_frame = gray_pic
	    else:
	        # absdiff把两幅图的差的绝对值输出到另一幅图上面来
	        img_delta = cv2.absdiff(pre_frame, gray_pic)
	        # threshold阈值函数(原图像应该是灰度图,对像素值进行分类的阈值,当像素值高于（有时是小于）阈值时应该被赋予的新的像素值,阈值方法)
	        thresh = cv2.threshold(img_delta, 30, 255, cv2.THRESH_BINARY)[1]
	        # 用一下腐蚀与膨胀
	        thresh = cv2.dilate(thresh, None, iterations=2)
	        # findContours检测物体轮廓(寻找轮廓的图像,轮廓的检索模式,轮廓的近似办法)
	        image, contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	        for c in contours:
	            # 设置敏感度
	            # contourArea计算轮廓面积
	            if cv2.contourArea(c) < 1000:
	                continue
	            else:
	                print(time.strftime("%H:%M:%S",time.localtime(time.time())))
	                print("探测到物体！！！")
	                # 保存图像
	                TI = time.strftime('%Y-%m-%d', time.localtime(time.time()))
	                # cv2.imwrite("D:\\python\\first_j\\" + "JC"+TI+ '.jpg', frame)
	                break
	        pre_frame = gray_pic
	 
	    if cv2.waitKey(1) & 0xFF == ord('q'):
	        break
	camera.release()
	cv2.destroyAllWindows()
