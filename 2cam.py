import cv2

cam0 = cv2.VideoCapture(0)
cam1 = cv2.VideoCapture(1)

# windows7 + python3.7+ opencv 3.4
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# Raspberry pi+ python2.7+opencv 2.4.9
fourcc = cv2.cv.CV_FOURCC('m', 'p', '4', 'v')
out0 = cv2.VideoWriter('out0.avi', fourcc, 20.0, (640, 480))
out1 = cv2.VideoWriter('out1.avi', fourcc, 20.0, (640, 480))

s0,s1 = False,False
while True:
    ret0, frame0 = cam0.read()
    ret1, frame1 = cam1.read()
    out0.write(frame0)
    out1.write(frame1)
    cv2.imshow('cam0',frame0)
    cv2.imshow('cam1',frame1)
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

cam0.release()
cam1.release()
out0.release()
out1.release()
cv2.destroyAllWindows()
