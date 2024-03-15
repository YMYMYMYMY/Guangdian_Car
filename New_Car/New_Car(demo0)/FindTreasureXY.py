import cv2
import numpy as np
import os

cornerLocationPoint = list()
treasureXY = list()
blueLowHSV = np.array([90, 100, 100])
blueHighHSV = np.array([124, 255, 255])
# red1
redLowHSV1 = np.array([160, 43, 60])
redHighHSV1 = np.array([180, 255, 255])
# red2
redLowHSV2 = np.array([0, 43, 60])
redHighHSV2 = np.array([5, 255, 255])
cap = cv2.VideoCapture(0)


def findTreasureXY0():
    while cap.isOpened():
        # 逐帧读取视频
        ret, frame = cap.read()

        if ret:
            # 在这里对每一帧进行处理
            # 将图像转换为灰度图像
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # 进行边缘检测
            edges = cv2.Canny(gray, 200, 300)

            # 轮廓提取
            contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cornerLocationPoint.clear()
            # 遍历轮廓
            for contour in contours:
                # 计算轮廓的边界框
                center, WH, _ = cv2.minAreaRect(contour)  # 找最小外接矩形
                w = WH[0]
                h = WH[1]
                if w > 40 or h > 40 or w < 20 or h < 20:   # 过大过小直接过滤
                    continue

                # 判断边界框是否接近正方形
                if abs(w - h) < 5:
                    # 绘制边界框
                    x = center[0]
                    y = center[1]

                    # NMS
                    tag = 1
                    for point in cornerLocationPoint:
                        x1 = point[0]
                        y1 = point[1]
                        r = pow(pow(x1 - x, 2) + pow(y1 - y, 2), 0.5)
                        if r < 20:
                            tag = 0
                            break
                    if tag:
                        cv2.rectangle(frame, (int(x - w / 2), int(y - h / 2)), (int(x + w / 2), int(y + h / 2)),
                                      (0, 255, 0), 2)
                        cornerLocationPoint.append([x, y, w, h])

            # 显示帧
            cv2.imshow('Camera', frame)
            cv2.waitKey(2)

            if len(cornerLocationPoint) == 4:
                # 排序
                cornerLocationPoint.sort(key=lambda member: member[0], reverse=False)
                cache = list()
                if cornerLocationPoint[0][1] < cornerLocationPoint[1][1]:
                    leftTop = cornerLocationPoint.pop(0)
                    leftBottom = cornerLocationPoint.pop(0)
                    cache.append(leftTop)
                else:
                    leftTop = cornerLocationPoint.pop(1)
                    leftBottom = cornerLocationPoint.pop(0)
                    cache.append(leftTop)
                cornerLocationPoint.sort(key=lambda member: member[1], reverse=False)
                rightTop = cornerLocationPoint.pop(0)
                rightBottom = cornerLocationPoint.pop(0)
                cache.append(rightTop)
                cache.append(leftBottom)
                cache.append(rightBottom)

                # 左上  右上  左下  右下
                X = [cache[0][0], cache[1][0], cache[2][0], cache[3][0]]
                Y = [cache[0][1], cache[1][1], cache[2][1], cache[3][1]]

                # 透视变换
                pic1 = np.float32([[X[0], Y[0]], [X[1], Y[1]], [X[2], Y[2]], [X[3], Y[3]]])
                pic2 = np.float32([[0, 0], [540, 0], [0, 540], [540, 540]])
                Matrix = cv2.getPerspectiveTransform(pic1, pic2)
                perspectivePic = cv2.warpPerspective(frame, Matrix, (540, 540))
                # cv2.imshow("PerspectiveTransform", perspectivePic)

                # 抵消平均误差
                width = (cache[0][2] + cache[1][2] + cache[2][2] + cache[3][2]) / 4
                height = (cache[0][3] + cache[1][3] + cache[2][3] + cache[3][3]) / 4
                # 截取迷宫区域
                cropped_image = perspectivePic[int(height * 2):int(540 - height * 2),
                                int(width * 2):int(540 - width * 2)]

                # 将彩色图像转换为灰度图像
                perspectiveGRAYPic = cv2.cvtColor(cropped_image, cv2.COLOR_BGR2GRAY)
                # 应用阈值处理，将灰度图像二值化为黑白图像
                _, binary_image = cv2.threshold(perspectiveGRAYPic, 100, 255, cv2.THRESH_BINARY)  # 光照调整
                cv2.imshow("THRESH_BINARY", binary_image)

                contours, hierarchy = cv2.findContours(binary_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

                treasureXY.clear()

                # 获取图像的宽度和高度
                w, h = perspectiveGRAYPic.shape
                # 计算每个小块的宽度和高度
                unitW = int(w/ 10)
                unitH = int(h/ 10)
                perspectiveRGBPic = cv2.cvtColor(perspectiveGRAYPic, cv2.COLOR_GRAY2RGB)
                # 使用嵌套循环来遍历图像，并划分为100个小块
                for i in range(0, h, unitH):
                    for j in range(0, w, unitW):
                        # 提取当前块的左上角和右下角坐标
                        x1, y1 = j, i
                        x2, y2 = j + unitW, i + unitH
                        # 在图像上绘制矩形框
                        cv2.rectangle(perspectiveRGBPic, (x1, y1), (x2, y2), (0, 255, 0), 2)  # 这里使用绿色框

                countXY = 0

                for contour in contours:
                    (x, y), radius = cv2.minEnclosingCircle(contour)
                    if 8 < radius < 15:
                        center = (int(x), int(y))
                        radius = int(radius)
                        cv2.circle(perspectiveRGBPic, center, radius, (0, 0, 255), 2)
                        countXY = countXY + 1
                        x = int(x / unitW) * 2 + 1
                        y = int(y / unitH) * 2 + 1
                        treasureXY.append([int(y), int(x)])
                cv2.imshow('DONE', perspectiveRGBPic)
                if countXY == 8:
                    TC = 0
                    teamImage = perspectivePic[300:550, 0:100]
                    hsv = cv2.cvtColor(teamImage, cv2.COLOR_BGR2HSV)

                    picRedHSV = cv2.inRange(hsv, lowerb=redLowHSV1, upperb=redHighHSV1) + cv2.inRange(hsv,
                                                                                                      lowerb=redLowHSV2,
                                                                                                      upperb=redHighHSV2)
                    # 进行边缘检测
                    edgesRed = cv2.Canny(picRedHSV, 200, 300)
                    # 轮廓提取
                    contoursRed, _ = cv2.findContours(edgesRed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    # 外层大色块
                    for contour in contoursRed:
                        # 找最小外接矩形
                        _, WH, _ = cv2.minAreaRect(contour)
                        w = WH[0]
                        h = WH[1]
                        if h > 20:  # 过小直接过滤
                            TC = 1

                    picBlueHSV = cv2.inRange(hsv, lowerb=blueLowHSV, upperb=blueHighHSV)
                    # 进行边缘检测
                    edgesBlue = cv2.Canny(picBlueHSV, 200, 300)
                    # 轮廓提取
                    contoursBlue, _ = cv2.findContours(edgesBlue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                    # 外层大色块
                    for contour in contoursBlue:
                        # 找最小外接矩形
                        _, WH, _ = cv2.minAreaRect(contour)
                        w = WH[0]
                        h = WH[1]
                        if h > 20:  # 过小直接过滤
                            TC = 2

                    cv2.imshow('teamImage', teamImage)
                    if TC == 0:
                        print("队伍颜色识别失败")
                    if TC == 1:
                        print("队伍颜色为：红")
                    if TC == 2:
                        print("队伍颜色为：蓝")

                    print("识别出的宝藏个数：", len(treasureXY))
                    print("识别出的宝藏坐标：", treasureXY)
                    key = cv2.waitKey(0)
                    # 按下 'Q' 键重新识别
                    if key == ord('Q') or key == ord('q'):
                        # 释放资源
                        cv2.destroyAllWindows()
                        continue
                    # 释放资源
                    cap.release()
                    cv2.destroyAllWindows()
                    return treasureXY,TC
                


        else:
            print("摄像头ret有问题")
            break

def findTreasureXY():
    if os.path.exists('treasure_data.npy'):
        # 如果文件存在，则直接加载数据并打印坐标
        treasure_data = np.load('treasure_data.npy', allow_pickle=True).item()
        treasureXY = treasure_data['treasure_list']
        teamColor = treasure_data['team_color']
        print(treasureXY)
        print(teamColor)
        cap.release()
        cv2.destroyAllWindows()
        return treasureXY,teamColor


    else:
        # 如果文件不存在，则进行拍照识别等操作
        treasureXY = []
        teamColor = 0
        # findTreasureXY()

        FfindTreasureXY= findTreasureXY0()
        treasure_list = FfindTreasureXY[0]
        teamColor = FfindTreasureXY[1]

        # 根据识别结果生成坐标数据
        # treasure_list = ...
        # teamColor = ...
        # 保存数据到文件
        treasure_data = {
            'treasure_list': treasure_list,
            'team_color': teamColor
        }
        np.save('treasure_data.npy', treasure_data)
        #print(treasure_list)
        #print(teamColor)
        return treasure_list,teamColor

#FfindTreasureXY = findTreasureXY()
#treasure_list = FfindTreasureXY[0]
#teamColor  = FfindTreasureXY[1]
#print("QwQ")
#print(treasure_list)
#print(teamColor)

findTreasureXY()