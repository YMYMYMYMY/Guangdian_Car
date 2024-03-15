import FindNearestTreasure
import os
import MoveControl
from FindTreasureXY import findTreasureXY
from FindNearestTreasure import TreasureDetector
from JudgeTreasure import judgeTreasure
import time

import cv2
import numpy as np
import time

#





pathList4Draw = list()
END = 0
numPart = 1


#treasure_list, teamColor = [[17, 17], [15, 11], [15, 5], [13, 9], [7, 11], [5, 15], [5, 9], [3, 3]], 1
FfindTreasureXY = findTreasureXY()
treasure_list = FfindTreasureXY[0]
teamColor  = FfindTreasureXY[1]



TD = TreasureDetector(0)
TD.classifyXY(treasure_list)





#def judgeTreasure():
#    global i
#    if i == 1:
#        i = i + 1
#        return 2
#    if i == 2:
#        i = i + 1
#        return 1
#    if i == 3:
#        i = i + 1
#        return 3
#    if i == 4:
#        i = i + 1
#        return 1
#    if i == 5:
#        i = i + 1
#        return 1
#    if i == 6:
#        i = i + 1
#        return 1


treasurePath, orientPath = TD.findNearestTreasurePoint(numPart, FindNearestTreasure.BEGIN_POINT_X,
    FindNearestTreasure.BEGIN_POINT_Y)
pathList4Draw.append(treasurePath)
MoveControl.move(orientPath)
#time.sleep(2)
print("TNT")
cvResult = judgeTreasure()
print("QwQ")
print(cvResult)

MoveControl.cvResultMove(cvResult, teamColor=teamColor)
print("###")
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
