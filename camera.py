 #!/usr/bin/python3

from collections import  deque
import numpy as np
#import imutils
import cv2
import time

#import serial
#ser = serial.Serial('/dev/ttyUSB1',9600,timeout=1)

def front_camera(color):
    while True:
        if color == "R":
            #设定red阈值，HSV空间
            Lower = np.array([150, 46, 46])#0
            Upper = np.array([180, 255, 255])#10
        elif color == "G":
            #设定green阈值，HSV空间
            Lower = np.array([40, 95, 95])#40, 95, 95
            Upper = np.array([100, 255, 255])#100, 255, 255
        elif color == "B":
            #设定blue阈值，HSV空间
            Lower = np.array([90, 43, 46])
            Upper = np.array([114, 255, 255])
        else:
            print("we don't have this color")


        #初始化追踪点的列表
        mybuffer = 64
        pts = deque(maxlen=mybuffer)

        #打开摄像头
        camera = cv2.VideoCapture(1)
        #等待两秒
        #time.sleep(2)


        #读取帧
        (ret, frame) = camera.read()
        cv2.imshow('Frame', frame)
        #判断是否成功打开摄像头
        if not ret:
            print ('No Camera')

        #转到HSV空间
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        #根据阈值构建掩膜
        mask = cv2.inRange(hsv, Lower, Upper)
        #腐蚀操作
        mask = cv2.erode(mask, None, iterations=2)
        #膨胀操作，其实先腐蚀再膨胀的效果是开运算，去除噪点
        mask = cv2.dilate(mask, None, iterations=2)
        #轮廓检测
        cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)[-2]
        #初始化瓶盖圆形轮廓质心

        center = None
        #如果存在轮廓
        if len(cnts) > 0:
            #找到面积最大的轮廓
            c = max(cnts, key = cv2.contourArea)
            #确定面积最大的轮廓的外接圆
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            #计算轮廓的矩
            print(y)
            print(x)

            M = cv2.moments(c)
            #计算质心
            center = (int(M["m10"]/M["m00"]), int(M["m01"]/M["m00"]))
            #只有当半径大于10时，才执行画图
            if radius > 10:
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 0, 255), -1)
                #把质心添加到pts中，并且是添加到列表左侧
                pts.appendleft(center)



        cv2.imshow('Frame', frame)
        cv2.waitKey(10)

    return x,y

a = front_camera("B")