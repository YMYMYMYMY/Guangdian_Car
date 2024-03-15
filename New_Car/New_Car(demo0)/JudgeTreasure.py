import cv2
import numpy as np
import time

# red1
redLowHSV1 = np.array([160, 43, 60])
redHighHSV1 = np.array([180, 255, 255])
# red2
redLowHSV2 = np.array([0, 43, 60])
redHighHSV2 = np.array([5, 255, 255])
# green
greenLowHSV = np.array([40 ,80, 80])
greenHighHSV = np.array([80, 255, 255])
# blue
# blueLowHSV = np.array([100, 220, 40])
blueLowHSV = np.array([90, 100, 100])
blueHighHSV = np.array([124, 255, 255])
# yellow
yellowLowHSV = np.array([20, 43, 46])
yellowHighHSV = np.array([38, 255, 255])

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

