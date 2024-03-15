###########################################################################
#代码说明
#文章架构：
#代码分为主函数（main.py）、藏宝图识别（FindTreasureXY.py）、路径规划(FindNearestTreasure.py)、宝藏识别(JudgeTreasure.py)、运动控制(MoveControl.py)五个部分
############################################################
#mian函数主要功能：搭建整个程序运行的框架，对各个函数进行导入，从而完成整个程序的运行。


import FindNearestTreasure
import os
import MoveControl
from FindTreasureXY import findTreasureXY
from FindNearestTreasure import TreasureDetector
from JudgeTreasure import judgeTreasure
import time
import cv2
import numpy as np



pathList4Draw = list()
END = 0
numPart = 1


FfindTreasureXY = findTreasureXY()
treasure_list = FfindTreasureXY[0]
teamColor  = FfindTreasureXY[1]



TD = TreasureDetector(0)
TD.classifyXY(treasure_list)


treasurePath, orientPath = TD.findNearestTreasurePoint(numPart, FindNearestTreasure.BEGIN_POINT_X,
    FindNearestTreasure.BEGIN_POINT_Y)
pathList4Draw.append(treasurePath)
MoveControl.move(orientPath)
#time.sleep(2)
cvResult = judgeTreasure()
print(cvResult)

MoveControl.cvResultMove(cvResult, teamColor=teamColor)
carResult = TD.updateMazeMap(numPart, cvResult, treasurePath[len(treasurePath) - 1], teamColor, treasurePath[len(treasurePath) - 2])


while 1:
    numPart, directX, directY, path, convertPath = carResult
    pathList4Draw.append(path)
    MoveControl.move(convertPath)
    #time.sleep(2)
    cvResult = judgeTreasure()
    print(cvResult)
    MoveControl.cvResultMove(cvResult, teamColor=teamColor)
    carResult = TD.updateMazeMap(numPart, cvResult, path[len(path) - 1], teamColor, path[len(path) - 2])

    # 最后一段路
    if carResult[0] == END:
        _, _, _, path, convertPath = carResult
        pathList4Draw.append(path)  # 画图功能，可以注释掉。
        MoveControl.move(convertPath)
        break
