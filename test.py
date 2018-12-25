import numpy as np
import cv2
 
img = cv2.imread('timg.jpg',0)
# cv2.imshow('image',img)
# k = cv2.waitKey(0)
# if k == 27:         # wait for ESC key to exit
#     cv2.destroyAllWindows()
# elif k == ord('s'): # wait for 's' key to save and exit
#     cv2.imwrite('kyriegray.jpg',img)
#     cv2.destroyAllWindows()
print (img.shape)

print (img.size)

print (img.dtype)
# uint8
# 在debug的时候，dtype很重要