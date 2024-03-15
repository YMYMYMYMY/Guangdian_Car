#这段代码是一个基于 OpenCV 的图像处理和边缘检测程序，在实时视频流中检测特定颜色的物体，并对其进行边缘检测。
#定义了五个颜色的HSV范围。HSV（色相、饱和度、亮度）是一种颜色表示方式。每种颜色都有一个低阈值和高阈值的HSV范围。
# 这些颜色包括红色、绿色、蓝色和黄色。这些范围将用于在视频流中检测特定颜色的物体。
#定义常量：
#BLUE_YELLOW、BLUE_GREEN、RED_GREEN 和 RED_YELLOW 是用于标记不同的颜色情况的常量。
#定义 judgeTreasure 函数：
#这个函数是整个程序的主要逻辑部分。
#cap 是用于从摄像头捕获视频的对象。
#while 循环在视频流处于打开状态时运行。
#在循环中，程序读取视频流的帧。
#每帧都会转换为HSV颜色空间，然后使用定义的颜色范围来创建掩码图像，以突出特定颜色的物体。
#然后，程序对突出显示的颜色进行边缘检测，找到这些物体的轮廓。
#接下来，程序会处理检测到的轮廓，找到最小外接矩形。

import cv2
import numpy as np
import time

# red1
redLowHSV1 = np.array([156, 45, 45])
redHighHSV1 = np.array([180, 255, 255])
# red2
redLowHSV2 = np.array([0, 45, 45])
redHighHSV2 = np.array([12, 255, 255])
# green
greenLowHSV = np.array([40 ,60, 30])
greenHighHSV = np.array([85, 255, 255])
# blue
# blueLowHSV = np.array([100, 220, 40])
blueLowHSV = np.array([90, 95, 75])
blueHighHSV = np.array([155, 255, 255])
# yellow
yellowLowHSV = np.array([20, 30, 50])
yellowHighHSV = np.array([34, 255, 255])

BLUE_YELLOW = 2  # 蓝色真
BLUE_GREEN = 4  # 蓝色假
RED_GREEN = 1  # 红色真
RED_YELLOW = 3  # 红色假



def judgeTreasure():
    print("WOW")
    start_time = time.time()
    judge_treasure_return = False
    cap = cv2.VideoCapture(0)
    #cap.release()
    tag = 0
    while cap.isOpened():
        # 逐帧读取视频
        ret, frame = cap.read()
        if ret:
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            # 对图片加上hsv # mask是只突出指定颜色的图片
            picBlueHSV = cv2.inRange(hsv, lowerb=blueLowHSV, upperb=blueHighHSV)
            picRedHSV = cv2.inRange(hsv, lowerb=redLowHSV1, upperb=redHighHSV1) + cv2.inRange(hsv, lowerb=redLowHSV2,
                                                                                              upperb=redHighHSV2)
            picYellowHSV = cv2.inRange(hsv, lowerb=yellowLowHSV, upperb=yellowHighHSV)
            picGreenHSV = cv2.inRange(hsv, lowerb=greenLowHSV, upperb=greenHighHSV)

            #cv2.imshow("picBlueHSV", picBlueHSV)
            #cv2.imshow("picRedHSV", picRedHSV)
            #cv2.imshow("picYellowHSV", picYellowHSV)
            #cv2.imshow("picGreenHSV", picGreenHSV)

            # 进行边缘检测
            edges = cv2.Canny(picBlueHSV, 200, 300)
            # 轮廓提取
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # 外层大色块
            for contour in contours:
                # 找最小外接矩形
                _, WH, _ = cv2.minAreaRect(contour)
                w = WH[0]
                h = WH[1]
                if h > 40:  # 过小直接过滤
                    # 定义腐蚀操作的结构元素
                    kernel = np.ones((3, 3), np.uint8)

                    # 进行腐蚀操作
                    eroded_image = cv2.erode(picYellowHSV, kernel, iterations=1)
                    edges = cv2.Canny(picYellowHSV, 200, 300)
                    contours1, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    # 内层小色块
                    for contour1 in contours1:
                        # 找最小外接矩形
                        _, WH, _ = cv2.minAreaRect(contour1)
                        w = WH[0]
                        if w > 20:  # 过小直接过滤
                            #cv2.waitKey(0)
                            cv2.destroyAllWindows()
                            now_time = time.time()
                            return BLUE_YELLOW
                    edges = cv2.Canny(picGreenHSV, 200, 300)
                    contours2, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    for contour2 in contours2:
                        # 找最小外接矩形
                        center, WH, _ = cv2.minAreaRect(contour2)
                        w = WH[0]
                        if w > 20:  # 过小直接过滤
                            #cv2.waitKey(0)
                            cv2.destroyAllWindows()
                            now_time = time.time()
                            return BLUE_GREEN
            # 进行边缘检测
            edges = cv2.Canny(picRedHSV, 200, 300)
            # 轮廓提取
            contours3, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            # 外层大色块
            for contour3 in contours3:
                # 找最小外接矩形
                _, WH, _ = cv2.minAreaRect(contour3)
                w = WH[0]
                h = WH[1]
                if h > 40:  # 过小直接过滤
                    edges = cv2.Canny(picGreenHSV, 200, 300)
                    contours5, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    for contour5 in contours5:
                        # 找最小外接矩形
                        _, WH, _ = cv2.minAreaRect(contour5)
                        w = WH[0]
                        if w > 20:  # 过小直接过滤
                            #cv2.waitKey(0)
                            cv2.destroyAllWindows()
                            now_time = time.time()
                            return RED_GREEN
                    edges = cv2.Canny(picYellowHSV, 200, 300)
                    contours4, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    # 内层小色块
                    for contour4 in contours4:
                        # 找最小外接矩形
                        _, WH, _ = cv2.minAreaRect(contour4)
                        w = WH[0]
                        if w > 20:  # 过小直接过滤
                            #cv2.waitKey(0)
                            cv2.destroyAllWindows()
                            now_time = time.time()
                            return RED_YELLOW
                            


            if judgeTreasure is not None:
                judge_treasure_return = True
                now_time = time.time()

        if now_time - start_time > 4:
            break
    cap.release()  # 释放摄像头资源
    cv2.destroyAllWindows()


#i = judgeTreasure()
#print(i)

        #if judgeTreasure is not None:
         #   Judge_Treasure_Return = True
        #else:
         #   Judge_Treasure_Return = False
          #  while Judge_Treasure_Return == True:
           #     # time.sleep(10)
            #    cap.release()  # 释放摄像头资源
             #   cv2.destroyAllWindows()

