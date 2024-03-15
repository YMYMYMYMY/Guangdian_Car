#从MazeMap和MoveControl模块中导入内容。
#从Python的内建库中导入deepcopy
#常量定义:
#有关迷宫的起点、终点、宝藏类别、方向和旋转方向的常量定义。
#迷宫地图:
#使用deepcopy复制MazeMap模块中定义的MAP。
#查找函数:
#findImportantPoints(): 用于找到迷宫中的岔路口。
#find2WallsPoints(): 查找有两面墙的点。
#findSymmetricalPoint(): 返回输入点的中心对称点。

import MazeMap
import MoveControl
from copy import deepcopy

BEGIN_POINT_X = 19
BEGIN_POINT_Y = 1
END_POINT_X = 1
END_POINT_Y = 19
# 象限
FIRST = 1
SECOND = 2
THIRD = 3
FOURTH = 4
# 宝藏类别
TRUE_RED = 1
TRUE_BLUE = 2
FALSE_RED = 3
FALSE_BLUE = 4
# 方向
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3
# 旋转方向
GO_STRAIGHT = 0
TURN_RIGHT = 1
TURN_LEFT = 3

mazeMap = deepcopy(MazeMap.MAP)  # 迷宫地图
Red = 1
Blue = 2


# 找出岔路口的点
def findImportantPoints():
    MAP = MazeMap.MAP
    importantList = list()
    for x in range(1, 20):
        for y in range(1, 20):
            count = 0
            if MAP[x][y] == 1:
                continue
            if MAP[x - 1][y] == 0:
                count = count + 1
            if MAP[x][y + 1] == 0:
                count = count + 1
            if MAP[x + 1][y] == 0:
                count = count + 1
            if MAP[x][y - 1] == 0:
                count = count + 1
            if count > 2:
                importantList.append([x, y])
    return importantList


# 找出两面墙的点
def find2WallsPoints():
    MAP = MazeMap.MAP
    twoWallsPointsList = list()
    for x in range(1, 20):
        for y in range(1, 20):
            count = 0
            if MAP[x][y] == 1:
                continue
            if MAP[x - 1][y] == 0:
                count = count + 1
            if MAP[x][y + 1] == 0:
                count = count + 1
            if MAP[x + 1][y] == 0:
                count = count + 1
            if MAP[x][y - 1] == 0:
                count = count + 1
            if count == 2:
                twoWallsPointsList.append([x, y])
    return twoWallsPointsList


def findSymmetricalPoint(input_x, input_y):  # 找到中心对称的点
    return 20 - input_x, 20 - input_y


def setAnotherPathBlock(xy, nearXY):
    x = xy[0]
    y = xy[1]
    # anotherX = nearXY[0]
    # anotherY = nearXY[1]
    MAP = MazeMap.MAP
    if MAP[x - 1][y] == 0 and [x - 1, y] != nearXY:
        mazeMap[x - 1][y] = 1
    elif MAP[x][y + 1] == 0 and [x, y + 1] != nearXY:
        mazeMap[x][y + 1] = 1
    elif MAP[x + 1][y] == 0 and [x + 1, y] != nearXY:
        mazeMap[x + 1][y] = 1
    elif MAP[x][y - 1] == 0 and [x, y - 1] != nearXY:
        mazeMap[x][y - 1] = 1


class TreasureDetector:
    def __init__(self, count):
        self.count = count
        self.Intersection_coordinates = findImportantPoints()
        self.twoWallsPoints = find2WallsPoints()
        self.firstQuadrantList = list()
        self.secondQuadrantList = list()
        self.thirdQuadrantList = list()
        self.fourthQuadrantList = list()
        # 尝试寻找最短路径的存储数据结构
        self.searchPath = list()
        self.orientPath = list()

    def classifyXY(self, treasure_list):  # 对于找到的宝藏坐标list进行象限的分类
        for xy in treasure_list:
            x, y = xy
            if x > 10 > y:
                self.firstQuadrantList.append(xy)
            if x > 10 and y > 10:
                self.secondQuadrantList.append(xy)
            if x < 10 and y < 10:
                self.thirdQuadrantList.append(xy)
            if x < 10 < y:
                self.fourthQuadrantList.append(xy)

    def findOneQuadrantXY(self, num):  # 返回某个象限的XY坐标的list
        if num == 1:
            return self.firstQuadrantList
        if num == 2:
            return self.secondQuadrantList
        if num == 3:
            return self.thirdQuadrantList
        if num == 4:
            return self.fourthQuadrantList

    def updateMazeMap(self, numPart, cvResult, xy, teamColor, nearXY):  # 更新mazeMap
        x, y = xy
        mazeMap[x][y] = 1
        if self.twoWallsPoints.count(xy) == 1:
            setAnotherPathBlock(xy, nearXY)
        if cvResult is None:
            print("该点宝物识别失败或无宝物")
            MoveControl.turnBack()
        convX, convY = findSymmetricalPoint(x, y)
        if teamColor == Red:
            if numPart == FIRST:
                if cvResult == TRUE_RED:
                    self.firstQuadrantList.remove([x, y])
                    self.count = self.count + 1
                    if len(self.firstQuadrantList) == 0:
                        path, convertPath = self.findNearestTreasurePoint(SECOND, x, y)
                        nextX, nextY = path[len(path) - 1]
                        return [SECOND, nextX, nextY, path, convertPath]
                    anotherX, anotherY = self.firstQuadrantList.pop()
                    mazeMap[anotherX][anotherY] = 1
                    self.fourthQuadrantList.remove([convX, convY])
                    mazeMap[convX][convY] = 1
                    path, convertPath = self.findNearestTreasurePoint(SECOND, x, y)
                    nextX, nextY = path[len(path) - 1]
                    return [SECOND, nextX, nextY, path, convertPath]
                if cvResult == FALSE_RED or cvResult is None:
                    self.firstQuadrantList.remove([x, y])
                    if len(self.firstQuadrantList) == 0:
                        path, convertPath = self.findNearestTreasurePoint(SECOND, x, y)
                        nextX, nextY = path[len(path) - 1]
                        return [SECOND, nextX, nextY, path, convertPath]
                    anotherX, anotherY = self.firstQuadrantList.pop()
                    mazeMap[anotherX][anotherY] = 1
                    self.fourthQuadrantList.remove([convX, convY])
                    mazeMap[convX][convY] = 1
                    path, convertPath = self.findNearestTreasurePoint(SECOND, x, y)
                    nextX, nextY = path[len(path) - 1]
                    return [SECOND, nextX, nextY, path, convertPath]
                if cvResult == TRUE_BLUE or cvResult is None:
                    self.firstQuadrantList.remove([x, y])
                    anotherX, anotherY = self.firstQuadrantList[0]
                    fourthX, fourthY = self.fourthQuadrantList.pop(1 - self.fourthQuadrantList.index([convX, convY]))
                    mazeMap[fourthX][fourthY] = 1
                    path, convertPath = self.findPath(x, y, anotherX, anotherY)
                    return [FIRST, anotherX, anotherY, path, convertPath]
                if cvResult == FALSE_BLUE or cvResult is None:
                    self.firstQuadrantList.remove([x, y])
                    anotherX, anotherY = self.firstQuadrantList[0]
                    fourthX, fourthY = self.fourthQuadrantList.pop(1 - self.fourthQuadrantList.index([convX, convY]))
                    mazeMap[fourthX][fourthY] = 1
                    #fourthX, fourthY = self.fourthQuadrantList.pop(0)
                    #mazeMap[fourthX][fourthY] = 1
                    #fourthX, fourthY = self.fourthQuadrantList.pop(0)
                    #mazeMap[fourthX][fourthY] = 1
                    path, convertPath = self.findPath(x, y, anotherX, anotherY)
                    return [FIRST, anotherX, anotherY, path, convertPath]
            if numPart == SECOND:
                if cvResult == TRUE_RED:
                    self.secondQuadrantList.remove([x, y])
                    self.count = self.count + 1
                    if len(self.secondQuadrantList) == 0:
                        if len(self.thirdQuadrantList) == 0:
                            path, convertPath = self.findNearestTreasurePoint(FOURTH, x, y)
                            nextX, nextY = path[len(path) - 1]
                            return [THIRD, nextX, nextY, path, convertPath]
                        else:
                            path, convertPath = self.findNearestTreasurePoint(THIRD, x, y)
                            nextX, nextY = path[len(path) - 1]
                            return [THIRD, nextX, nextY, path, convertPath]
                    else:
                        anotherX, anotherY = self.secondQuadrantList.pop()
                        mazeMap[anotherX][anotherY] = 1
                        self.thirdQuadrantList.remove([convX, convY])
                        mazeMap[convX][convY] = 1
                        nextX, nextY = self.thirdQuadrantList[0]
                        path, convertPath = self.findNearestTreasurePoint(THIRD, x, y)
                        return [THIRD, nextX, nextY, path, convertPath]
                if cvResult == FALSE_RED:
                    self.secondQuadrantList.remove([x, y])
                    if len(self.secondQuadrantList) == 0:
                        path, convertPath = self.findNearestTreasurePoint(THIRD, x, y)
                        nextX, nextY = path[len(path) - 1]
                        return [THIRD, nextX, nextY, path, convertPath]
                    else:
                        anotherX, anotherY = self.secondQuadrantList.pop()
                        mazeMap[anotherX][anotherY] = 1
                        self.thirdQuadrantList.remove([convX, convY])
                        mazeMap[convX][convY] = 1
                        nextX, nextY = self.thirdQuadrantList[0]
                        path, convertPath = self.findNearestTreasurePoint(THIRD, x, y)
                        return [THIRD, nextX, nextY, path, convertPath]
                if cvResult == TRUE_BLUE or cvResult is None:
                    self.secondQuadrantList.remove([x, y])
                    thirdX, thirdY = self.thirdQuadrantList.pop(1 - self.thirdQuadrantList.index([convX, convY]))
                    mazeMap[thirdX][thirdY] = 1
                    anotherX, anotherY = self.secondQuadrantList[0]
                    path, convertPath = self.findPath(x, y, anotherX, anotherY)
                    return [SECOND, anotherX, anotherY, path, convertPath]
                if cvResult == FALSE_BLUE or cvResult is None:
                    self.secondQuadrantList.remove([x, y])
                    #mazeMap[convX][convY] = 1
                    #thirdX, thirdY = self.thirdQuadrantList.pop(0)
                    #mazeMap[thirdX][thirdY] = 1
                    # 获取 self.thirdQuadrantList 中与 [convX, convY] 这个坐标不同的第一个坐标 [thirdX, thirdY]
                    thirdX, thirdY = self.thirdQuadrantList.pop(1 - self.thirdQuadrantList.index([convX, convY]))
                    # 在迷宫地图的坐标 [thirdX, thirdY] 处设置为 1
                    mazeMap[thirdX][thirdY] = 1
                    anotherX, anotherY = self.secondQuadrantList[0]
                    path, convertPath = self.findPath(x, y, anotherX, anotherY)
                    return [SECOND, anotherX, anotherY, path, convertPath]
            if numPart == THIRD:
                if cvResult == TRUE_RED:
                    self.thirdQuadrantList.remove([x, y])
                    self.count = self.count + 1
                    if self.count == 3:
                        path, convertPath = self.findPath(x, y, END_POINT_X, END_POINT_Y)
                        return [0, END_POINT_X, END_POINT_Y, path, convertPath]
                    path, convertPath = self.findNearestTreasurePoint(FOURTH, x, y)
                    nextX, nextY = path[len(path) - 1]
                    return [FOURTH, nextX, nextY, path, convertPath]
                if cvResult == TRUE_BLUE or cvResult == FALSE_RED or cvResult == FALSE_BLUE or cvResult is None:
                    self.thirdQuadrantList.remove([x, y])
                    path, convertPath = self.findNearestTreasurePoint(FOURTH, x, y)
                    nextX, nextY = path[len(path) - 1]
                    return [FOURTH, nextX, nextY, path, convertPath]
            if numPart == FOURTH or cvResult is None:
                if cvResult == TRUE_RED:
                    self.fourthQuadrantList.remove([x, y])
                    path, convertPath = self.findPath(x, y, END_POINT_X, END_POINT_Y)
                    return [0, END_POINT_X, END_POINT_Y, path, convertPath]
        if teamColor == Blue:
            if numPart == FIRST:
                if cvResult == TRUE_BLUE:
                    self.firstQuadrantList.remove([x, y])
                    self.count = self.count + 1
                    if len(self.firstQuadrantList) == 0:
                        path, convertPath = self.findNearestTreasurePoint(SECOND, x, y)
                        nextX, nextY = path[len(path) - 1]
                        return [SECOND, nextX, nextY, path, convertPath]
                    anotherX, anotherY = self.firstQuadrantList.pop()
                    mazeMap[anotherX][anotherY] = 1
                    self.fourthQuadrantList.remove([convX, convY])
                    mazeMap[convX][convY] = 1
                    path, convertPath = self.findNearestTreasurePoint(SECOND, x, y)
                    nextX, nextY = path[len(path) - 1]
                    return [SECOND, nextX, nextY, path, convertPath]
                if cvResult == FALSE_BLUE or cvResult is None:
                    self.firstQuadrantList.remove([x, y])
                    if len(self.firstQuadrantList) == 0:
                        path, convertPath = self.findNearestTreasurePoint(SECOND, x, y)
                        nextX, nextY = path[len(path) - 1]
                        return [SECOND, nextX, nextY, path, convertPath]
                    anotherX, anotherY = self.firstQuadrantList.pop()
                    mazeMap[anotherX][anotherY] = 1
                    self.fourthQuadrantList.remove([convX, convY])
                    mazeMap[convX][convY] = 1
                    path, convertPath = self.findNearestTreasurePoint(SECOND, x, y)
                    nextX, nextY = path[len(path) - 1]
                    return [SECOND, nextX, nextY, path, convertPath]
                if cvResult == TRUE_RED or cvResult is None:
                    self.firstQuadrantList.remove([x, y])
                    anotherX, anotherY = self.firstQuadrantList[0]
                    fourthX, fourthY = self.fourthQuadrantList.pop(1 - self.fourthQuadrantList.index([convX, convY]))
                    mazeMap[fourthX][fourthY] = 1
                    path, convertPath = self.findPath(x, y, anotherX, anotherY)
                    return [FIRST, anotherX, anotherY, path, convertPath]
                if cvResult == FALSE_RED or cvResult is None:
                    self.firstQuadrantList.remove([x, y])
                    anotherX, anotherY = self.firstQuadrantList[0]
                    #fourthX, fourthY = self.fourthQuadrantList.pop(0)
                    fourthX, fourthY = self.fourthQuadrantList.pop(1 - self.fourthQuadrantList.index([convX, convY]))
                    mazeMap[fourthX][fourthY] = 1
                    #fourthX, fourthY = self.fourthQuadrantList.pop(0)
                   # mazeMap[fourthX][fourthY] = 1
                    path, convertPath = self.findPath(x, y, anotherX, anotherY)
                    return [FIRST, anotherX, anotherY, path, convertPath]
            if numPart == SECOND:
                if cvResult == TRUE_BLUE:
                    self.secondQuadrantList.remove([x, y])
                    self.count = self.count + 1
                    if len(self.secondQuadrantList) == 0:
                        if len(self.thirdQuadrantList) == 0:
                            path, convertPath = self.findNearestTreasurePoint(FOURTH, x, y)
                            nextX, nextY = path[len(path) - 1]
                            return [FOURTH, nextX, nextY, path, convertPath]
                        path, convertPath = self.findNearestTreasurePoint(THIRD, x, y)
                        nextX, nextY = path[len(path) - 1]
                        return [THIRD, nextX, nextY, path, convertPath]
                    anotherX, anotherY = self.secondQuadrantList.pop()
                    mazeMap[anotherX][anotherY] = 1
                    self.thirdQuadrantList.remove([convX, convY])
                    mazeMap[convX][convY] = 1
                    nextX, nextY = self.thirdQuadrantList[0]
                    path, convertPath = self.findNearestTreasurePoint(THIRD, x, y)
                    return [THIRD, nextX, nextY, path, convertPath]
                if cvResult == FALSE_BLUE:
                    self.secondQuadrantList.remove([x, y])
                    if len(self.secondQuadrantList) == 0:
                        path, convertPath = self.findNearestTreasurePoint(THIRD, x, y)
                        nextX, nextY = path[len(path) - 1]
                        return [THIRD, nextX, nextY, path, convertPath]
                    anotherX, anotherY = self.secondQuadrantList.pop()
                    mazeMap[anotherX][anotherY] = 1
                    self.thirdQuadrantList.remove([convX, convY])
                    mazeMap[convX][convY] = 1
                    nextX, nextY = self.thirdQuadrantList[0]
                    path, convertPath = self.findNearestTreasurePoint(THIRD, x, y)
                    return [THIRD, nextX, nextY, path, convertPath]
                if cvResult == TRUE_RED or cvResult is None:
                    self.secondQuadrantList.remove([x, y])
                    thirdX, thirdY = self.thirdQuadrantList.pop(1 - self.thirdQuadrantList.index([convX, convY]))
                    mazeMap[thirdX][thirdY] = 1
                    anotherX, anotherY = self.secondQuadrantList[0]
                    path, convertPath = self.findPath(x, y, anotherX, anotherY)
                    return [SECOND, anotherX, anotherY, path, convertPath]
                if cvResult == FALSE_RED or cvResult is None:
                    self.secondQuadrantList.remove([x, y])
                    mazeMap[convX][convY] = 1
                    #thirdX, thirdY = self.thirdQuadrantList.pop(0)
                    #mazeMap[thirdX][thirdY] = 1
                    #thirdX, thirdY = self.thirdQuadrantList.pop(0)
                    thirdX, thirdY = self.thirdQuadrantList.pop(1 - self.thirdQuadrantList.index([convX, convY]))
                    mazeMap[thirdX][thirdY] = 1
                    anotherX, anotherY = self.secondQuadrantList[0]
                    path, convertPath = self.findPath(x, y, anotherX, anotherY)
                    return [SECOND, anotherX, anotherY, path, convertPath]
            if numPart == THIRD:
                if cvResult == TRUE_BLUE:
                    self.thirdQuadrantList.remove([x, y])
                    self.count = self.count + 1
                    if self.count == 3:
                        path, convertPath = self.findPath(x, y, END_POINT_X, END_POINT_Y)
                        return [0, END_POINT_X, END_POINT_Y, path, convertPath]
                    path, convertPath = self.findNearestTreasurePoint(FOURTH, x, y)
                    nextX, nextY = path[len(path) - 1]
                    return [FOURTH, nextX, nextY, path, convertPath]
                if cvResult == TRUE_RED or cvResult == FALSE_BLUE or cvResult == FALSE_RED or cvResult is None:
                    self.thirdQuadrantList.remove([x, y])
                    path, convertPath = self.findNearestTreasurePoint(FOURTH, x, y)
                    nextX, nextY = path[len(path) - 1]
                    return [FOURTH, nextX, nextY, path, convertPath]
            if numPart == FOURTH:
                if cvResult == TRUE_BLUE or cvResult is None:
                    self.fourthQuadrantList.remove([x, y])
                    path, convertPath = self.findPath(x, y, END_POINT_X, END_POINT_Y)
                    return [0, END_POINT_X, END_POINT_Y, path, convertPath]

    def findNearestTreasurePoint(self, numPart, beginX, beginY):  # 针对num象限进行搜索最近的路径的坐标点
        index = 0  # 坐标点存储在list中的索引参数
        father_point = -1  # 广度优先搜索的父节点索引参数
        self.searchPath.clear()
        self.searchPath.append([beginX, beginY, index, father_point])  # 将起点加入list
        index += 1
        newMap = deepcopy(mazeMap)
        newMap[beginX][beginY] = 1  # 将加入list中的坐标对应的迷宫地图设置为1，表示此路已经经历过，不允许再次遍历
        p = 0  # 表示队列中首指针的索引，用于出队（并非真出队，只是访问该点），同时也是广度优先子节点的父节点索引
        chosenQuadrantList = self.findOneQuadrantXY(numPart)

        while p != index:  # 队列不空就循环广度优先搜索
            node = self.searchPath[p]
            x, y, _, _ = node
            # 遍历四周：若是路径可以走，则加入队列，若是目标点，则break跳出循环
            if newMap[x - 1][y] == 0:
                self.searchPath.append([x - 1, y, index, p])
                index += 1
                newMap[x - 1][y] = 1
                if [x - 1, y] in chosenQuadrantList:
                    break
            if newMap[x][y + 1] == 0:
                index += 1
                self.searchPath.append([x, y + 1, index, p])
                newMap[x][y + 1] = 1
                if [x, y + 1] in chosenQuadrantList:
                    break
            if newMap[x + 1][y] == 0:
                index += 1
                self.searchPath.append([x + 1, y, index, p])
                newMap[x + 1][y] = 1
                if [x + 1, y] in chosenQuadrantList:
                    break
            if newMap[x][y - 1] == 0:
                index += 1
                self.searchPath.append([x, y - 1, index, p])
                newMap[x][y - 1] = 1
                if [x, y - 1] in chosenQuadrantList:
                    break
            p += 1  # 继续遍历下一个坐标
        index -= 1  # 此时已经找到目标点
        path = list()  # 用于保存真正的路径

        node = self.searchPath[index]  # 反向去寻找父坐标，直到找到初始坐标
        while node[3] != -1:
            path.append([node[0], node[1]])
            node = self.searchPath[node[3]]
        path.append([node[0], node[1]])  # 初始坐标也加进来
        path.reverse()  # 反转list，正向输出
        print(path)
        print("路径长度：", len(path), "到达点：", path[len(path) - 1])
        convertPath = self.convert2OrientPath(deepcopy(path))
        return path, convertPath  # , convertPath

    def findPath(self, begin_x, begin_y, end_x, end_y):
        index = 0  # 坐标点存储在list中的索引参数
        father_point = -1  # 广度优先搜索的父节点索引参数
        self.searchPath.clear()
        self.searchPath.append([begin_x, begin_y, index, father_point])  # 将起点加入list
        index += 1
        newMap = deepcopy(mazeMap)
        newMap[begin_x][begin_y] = 1  # 将加入list中的坐标对应的迷宫地图设置为1，表示此路已经经历过，不允许再次遍历
        p = 0  # 表示队列中首指针的索引，用于出队（并非真出队，只是访问该点），同时也是广度优先子节点的父节点索引

        while p != index:  # 队列不空就循环广度优先搜索
            node = self.searchPath[p]
            x = node[0]
            y = node[1]
            # 遍历四周：若是路径可以走，则加入队列，若是目标点，则break跳出循环
            if newMap[x - 1][y] == 0:
                self.searchPath.append([x - 1, y, index, p])
                index += 1
                newMap[x - 1][y] = 1
                if x - 1 == end_x and y == end_y:
                    break
            if newMap[x][y + 1] == 0:
                index += 1
                self.searchPath.append([x, y + 1, index, p])
                newMap[x][y + 1] = 1
                if x == end_x and y + 1 == end_y:
                    break
            if newMap[x + 1][y] == 0:
                index += 1
                self.searchPath.append([x + 1, y, index, p])
                newMap[x + 1][y] = 1
                if x + 1 == end_x and y == end_y:
                    break
            if newMap[x][y - 1] == 0:
                index += 1
                self.searchPath.append([x, y - 1, index, p])
                newMap[x][y - 1] = 1
                if x == end_x and y - 1 == end_y:
                    break
            p += 1  # 继续遍历下一个坐标
        index -= 1  # 此时已经找到目标点
        path = list()  # 用于保存真正的路径

        node = self.searchPath[index]  # 反向去寻找父坐标，直到找到初始坐标
        while node[3] != -1:
            path.append([node[0], node[1]])
            node = self.searchPath[node[3]]
        path.append([node[0], node[1]])  # 初始坐标也加进来
        path.reverse()  # 反转list，正向输出
        print(path)
        print("路径长度：", len(path), "到达点：", path[len(path) - 1])
        convertPath = self.convert2OrientPath(deepcopy(path))
        return path, convertPath  # , convertPath

    def convert2OrientPath(self, path):
        orientationList = list()
        result = -1
        i = 0
        n = len(path)
        while i + 1 < n:
            runX = path[i + 1][0] - path[i][0]
            runY = path[i + 1][1] - path[i][1]
            if runX == 1 and runY == 0:
                result = DOWN
            if runX == 0 and runY == 1:
                result = RIGHT
            if runX == -1 and runY == 0:
                result = UP
            if runX == 0 and runY == -1:
                result = LEFT
            self.orientPath.append(result)
            i = i + 1
        print("路径方向：", self.orientPath)
        path.reverse()
        locationList = path
        destination = locationList[0]
        self.orientPath.reverse()
        reversedOrientPath = self.orientPath
        nowLocation = locationList.pop()
        nowOrientation = reversedOrientPath.pop()
        nextLocation = locationList.pop()
        nextOrientation = reversedOrientPath.pop()
        while nextLocation != destination:
            if nextOrientation - nowOrientation == 1 or nextOrientation - nowOrientation == -3:
                orientationList.append(TURN_RIGHT)
                nowOrientation = nextOrientation
                if len(reversedOrientPath) != 0:
                    nextOrientation = reversedOrientPath.pop()
                nowLocation = nextLocation
                nextLocation = locationList.pop()
                continue
            if nextOrientation - nowOrientation == -1 or nextOrientation - nowOrientation == 3:
                orientationList.append(TURN_LEFT)
                nowOrientation = nextOrientation
                if len(reversedOrientPath) != 0:
                    nextOrientation = reversedOrientPath.pop()
                nowLocation = nextLocation
                nextLocation = locationList.pop()
                continue
            if nextOrientation - nowOrientation == 0 and self.Intersection_coordinates.count(nextLocation) == 1:
                orientationList.append(GO_STRAIGHT)
            nowOrientation = nextOrientation
            if len(reversedOrientPath) != 0:
                nextOrientation = reversedOrientPath.pop()
            nowLocation = nextLocation
            nextLocation = locationList.pop()

        print("旋转方向：", orientationList)
        print("--------------------")


        return orientationList

