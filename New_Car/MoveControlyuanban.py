#* coding:UTF8 *
import RPi.GPIO as GPIO
import time
import YB_Pcb_Car  #导入Yahboom专门库文件
import Distance
#from JudgeTreasure import RED_GREEN, BLUE_YELLOW, BLUE_GREEN, RED_YELLOW
#
car = YB_Pcb_Car.YB_Pcb_Car()
#
BLUE_YELLOW = 2  # 蓝色真
BLUE_GREEN = 4  # 蓝色假
RED_GREEN = 1  # 红色真
RED_YELLOW = 3  # 红色假


Tracking_Right1 = 11  #X1A  右边第一个传感器
Tracking_Right2 = 7  #X2A  右边第二个传感器
Tracking_Left1 = 13  #X1B 左边第一个传感器
Tracking_Left2 = 15  #X2B 左边第二个传感器
#
GPIO.setmode(GPIO.BOARD)
#
GPIO.setwarnings(False)
#
GPIO.setup(Tracking_Left1, GPIO.IN)
GPIO.setup(Tracking_Left2, GPIO.IN)
GPIO.setup(Tracking_Right1, GPIO.IN)
GPIO.setup(Tracking_Right2, GPIO.IN)
#
turnList = list()
accomplishTag = 1
#
#
def distanceMove():
    distance = Distance.Distance()
    while distance > 10:
        tracking_function()
        distance = Distance.Distance()
    car.Car_Stop()
    time.sleep(2)
    return
#
#
 #遇到不是直行的路径，就来寻找方向指令，遇到转弯就回来查询转向，并按既定方向指令运动。
def move(orientList):
     #处理坐标，转化为控制
    global turnList, accomplishTag
    orientList.reverse()
    turnList = orientList
    car.Car_Stop()
    while accomplishTag:
        tracking_function()
    accomplishTag = 1
    distanceMove()
#
#
def goStraight():
    #电机驱动代码
    car.Car_Run(65, 65)
    time.sleep(0.3)
#
#
def turnRight():
    #电机驱动代码
    car.Car_Run(40, 40)
    time.sleep(0.5)
    car.Car_Spin_Right(200, 200)
    time.sleep(0.2)
    while 1:
        car.Car_Spin_Right(90, 90)
        time.sleep(0.01)
        Tracking_Left1Value = GPIO.input(Tracking_Left1)
        Tracking_Left2Value = GPIO.input(Tracking_Left2)
        Tracking_Right1Value = GPIO.input(Tracking_Right1)
        Tracking_Right2Value = GPIO.input(Tracking_Right2)
        #print(Tracking_Left1Value, Tracking_Left2Value, Tracking_Right1Value, Tracking_Right2Value)
        if Tracking_Left2Value == 0 or Tracking_Right1Value == 0:
            car.Car_Spin_Left(150, 150)
            time.sleep(0.2)
            car.Car_Stop()
            #time.sleep(0.2)
            break
    if len(turnList) == 0:
        global accomplishTag
        accomplishTag = 0
        beginTime = time.time()
        nowTime = time.time()
        #最后一个弯道后直行多久
        while nowTime - beginTime < 0.4:
            tracking_function()
            nowTime = time.time()
#
#
def turnLeft():
    #电机驱动代码
    car.Car_Run(40,40)
    time.sleep(0.5)
    car.Car_Spin_Left(200, 200)
    time.sleep(0.2)
    while 1:
        car.Car_Spin_Left(100, 100)
        time.sleep(0.01)
        Tracking_Left1Value = GPIO.input(Tracking_Left1)
        Tracking_Left2Value = GPIO.input(Tracking_Left2)
        Tracking_Right1Value = GPIO.input(Tracking_Right1)
        Tracking_Right2Value = GPIO.input(Tracking_Right2)
        #print(Tracking_Left1Value, Tracking_Left2Value, Tracking_Right1Value, Tracking_Right2Value)
        if Tracking_Left2Value == 0 or Tracking_Right1Value == 0:
            car.Car_Spin_Right(100, 100)
            time.sleep(0.15)
            car.Car_Stop()
            #time.sleep(0.2)
            break
    if len(turnList) == 0:
        global accomplishTag
        accomplishTag = 0
        beginTime = time.time()
        nowTime = time.time()
        while nowTime - beginTime < 0.4:
            tracking_function()
            nowTime = time.time()
#
#
def turnBack():
    car.Car_Spin_Right(90, 90)
    time.sleep(0.1)
    print("turn back")
    while 1:
        car.Car_Spin_Right(60, 90)
        time.sleep(0.02)
        Tracking_Left1Value = GPIO.input(Tracking_Left1)
        Tracking_Left2Value = GPIO.input(Tracking_Left2)
        Tracking_Right1Value = GPIO.input(Tracking_Right1)
        Tracking_Right2Value = GPIO.input(Tracking_Right2)
        #print(Tracking_Left1Value, Tracking_Left2Value, Tracking_Right1Value, Tracking_Right2Value)
        if Tracking_Left2Value == 0:
            car.Car_Spin_Left(65, 65)
            time.sleep(0.2)
            car.Car_Back(40,40)
            time.sleep(0.4)
            car.Car_Stop()
            
            break
#
#
def where2Go():
    orient = turnList.pop()
    print("pop orient:", orient)
    if orient == 1:
        turnRight()
    if orient == 3:
        turnLeft()
    if orient == 0:
        goStraight()
#
#
def tracking_function():
    #接收输入信号
    Tracking_Left1Value = GPIO.input(Tracking_Left1)
    Tracking_Left2Value = GPIO.input(Tracking_Left2)
    Tracking_Right1Value = GPIO.input(Tracking_Right1)
    Tracking_Right2Value = GPIO.input(Tracking_Right2)
#
    #print(Tracking_Left1Value, Tracking_Left2Value, Tracking_Right1Value, Tracking_Right2Value)
    #四路循迹引脚电平状态
    #1 0 0 0
    #1 1 0 0
    #处理右直角的转动
    if Tracking_Left1Value == 1 and Tracking_Left2Value == 0 and Tracking_Right1Value == 0 \
            and Tracking_Right2Value == 0 \
            or (
            Tracking_Left1Value == 1 and Tracking_Left2Value == 1 and Tracking_Right1Value == 0
            and Tracking_Right2Value == 0):
        where2Go()
#
    #四路循迹引脚电平状态
    #0 0 0 1
    #0 0 1 1
    #处理左直角的转动
    elif Tracking_Left1Value == 0 and Tracking_Left2Value == 0 and Tracking_Right1Value == 0 \
            and Tracking_Right2Value == 1 \
            or (
            Tracking_Left1Value == 0 and Tracking_Left2Value == 0 and Tracking_Right1Value == 1
            and Tracking_Right2Value == 1):
        where2Go()
#
    #四路循迹引脚电平状态
    #0 0 0 0
    #处理丁字口的转动
    elif Tracking_Left1Value == 0 and Tracking_Left2Value == 0 and Tracking_Right1Value == 0 \
            and Tracking_Right2Value == 0:
        where2Go()
#
    #四路循迹引脚电平状态
    #1 0 1 1
    #0 1 1 1
    #处理左小弯
    elif Tracking_Left1Value == 1 and Tracking_Left2Value == 0 and Tracking_Right1Value == 1 and Tracking_Right2Value == 1 \
            or Tracking_Left1Value == 0 and Tracking_Left2Value == 1 and Tracking_Right1Value == 1 and Tracking_Right2Value == 1:
        car.Car_Spin_Left(0, 500)
        time.sleep(0.03)
    #四路循迹引脚电平状态
    #1 1 0 1
    #1 1 1 0
    #处理右小弯
    elif Tracking_Left1Value == 1 and Tracking_Left2Value == 1 and Tracking_Right1Value == 0 and Tracking_Right2Value == 1 \
            or Tracking_Left1Value == 1 and Tracking_Left2Value == 1 and Tracking_Right1Value == 1 and Tracking_Right2Value == 0:
        car.Car_Spin_Right(500, 0)
        time.sleep(0.03)
#
    #四路循迹引脚电平状态
    #1 0 0 1
    #处理直线
    elif Tracking_Left1Value == 1 and Tracking_Left2Value == 0 and Tracking_Right1Value == 0 and Tracking_Right2Value == 1:
        car.Car_Run(65, 65)
        time.sleep(0.01)
#
    #当为1 1 1 1时小车直行
    elif Tracking_Left1Value == 1 and Tracking_Left2Value == 1 and Tracking_Right1Value == 1 and Tracking_Right2Value == 1:
        car.Car_Run(65, 65)
        time.sleep(0.01)
#


def tracking_function1():
    #接收输入信号
    Tracking_Left1Value = GPIO.input(Tracking_Left1)
    Tracking_Left2Value = GPIO.input(Tracking_Left2)
    Tracking_Right1Value = GPIO.input(Tracking_Right1)
    Tracking_Right2Value = GPIO.input(Tracking_Right2)
#
    #print(Tracking_Left1Value, Tracking_Left2Value, Tracking_Right1Value, Tracking_Right2Value)
    #四路循迹引脚电平状态
    #1 0 0 0
    #1 1 0 0
    #处理右直角的转动
    if Tracking_Left1Value == 1 and Tracking_Left2Value == 0 and Tracking_Right1Value == 0 \
            and Tracking_Right2Value == 0 \
            or (
            Tracking_Left1Value == 1 and Tracking_Left2Value == 1 and Tracking_Right1Value == 0
            and Tracking_Right2Value == 0):
        car.Car_Spin_Right(500, 0)
        time.sleep(0.08)
#
    #四路循迹引脚电平状态
    #0 0 0 1
    #0 0 1 1
    #处理左直角的转动
    elif Tracking_Left1Value == 0 and Tracking_Left2Value == 0 and Tracking_Right1Value == 0 \
            and Tracking_Right2Value == 1 \
            or (
            Tracking_Left1Value == 0 and Tracking_Left2Value == 0 and Tracking_Right1Value == 1
            and Tracking_Right2Value == 1):
        car.Car_Spin_Left(500, 0)
        time.sleep(0.08)
#
    #四路循迹引脚电平状态
    #0 0 0 0
    #处理丁字口的转动
    elif Tracking_Left1Value == 0 and Tracking_Left2Value == 0 and Tracking_Right1Value == 0 \
            and Tracking_Right2Value == 0:
        car.Car_Spin_Right(500, 0)
        time.sleep(0.08)
#
    #四路循迹引脚电平状态
    #1 0 1 1
    #0 1 1 1
    #处理左小弯
    elif Tracking_Left1Value == 1 and Tracking_Left2Value == 0 and Tracking_Right1Value == 1 and Tracking_Right2Value == 1 \
            or Tracking_Left1Value == 0 and Tracking_Left2Value == 1 and Tracking_Right1Value == 1 and Tracking_Right2Value == 1:
        car.Car_Spin_Left(0, 500)
        time.sleep(0.03)
    #四路循迹引脚电平状态
    #1 1 0 1
    #1 1 1 0
    #处理右小弯
    elif Tracking_Left1Value == 1 and Tracking_Left2Value == 1 and Tracking_Right1Value == 0 and Tracking_Right2Value == 1 \
            or Tracking_Left1Value == 1 and Tracking_Left2Value == 1 and Tracking_Right1Value == 1 and Tracking_Right2Value == 0:
        car.Car_Spin_Right(500, 0)
        time.sleep(0.03)
#
    #四路循迹引脚电平状态
    #1 0 0 1
    #处理直线
    elif Tracking_Left1Value == 1 and Tracking_Left2Value == 0 and Tracking_Right1Value == 0 and Tracking_Right2Value == 1:
        car.Car_Run(80, 80)
        time.sleep(0.01)
#
    #当为1 1 1 1时小车直行
    elif Tracking_Left1Value == 1 and Tracking_Left2Value == 1 and Tracking_Right1Value == 1 and Tracking_Right2Value == 1:
        car.Car_Run(65, 65)
        time.sleep(0.01)
    




def cvResultMove(cvResult, teamColor):
    if teamColor == 1:
        if cvResult == RED_GREEN:
            beginTime = time.time()
            nowTime = time.time()
#
            while nowTime - beginTime < 0.8:
                Tracking_Left1Value = GPIO.input(Tracking_Left1)
                Tracking_Left2Value = GPIO.input(Tracking_Left2)
                Tracking_Right1Value = GPIO.input(Tracking_Right1)
                Tracking_Right2Value = GPIO.input(Tracking_Right2)
                if Tracking_Left1Value == 1 and Tracking_Left2Value == 0 and Tracking_Right1Value == 0 and Tracking_Right2Value == 1:
                    car.Car_Run(50, 50)
                    time.sleep(0.01)
#
                    #当为1 1 1 1时小车直行
                elif Tracking_Left1Value == 1 and Tracking_Left2Value == 1 and Tracking_Right1Value == 1 and Tracking_Right2Value == 1:
                    car.Car_Run(30, 30)
                    time.sleep(1)
                    
                nowTime = time.time()
#
            turnBack()
            return
        if cvResult == RED_YELLOW or cvResult == BLUE_GREEN or cvResult == BLUE_YELLOW:
            turnBack()
            return
    if teamColor == 2:
        if cvResult == BLUE_YELLOW:
            beginTime = time.time()
            nowTime = time.time()
#
            while nowTime - beginTime < 0.8:
                Tracking_Left1Value = GPIO.input(Tracking_Left1)
                Tracking_Left2Value = GPIO.input(Tracking_Left2)
                Tracking_Right1Value = GPIO.input(Tracking_Right1)
                Tracking_Right2Value = GPIO.input(Tracking_Right2)
                if Tracking_Left1Value == 1 and Tracking_Left2Value == 0 and Tracking_Right1Value == 0 and Tracking_Right2Value == 1:
                    car.Car_Run(50, 50)
                    time.sleep(0.01)
#
                    #当为1 1 1 1时小车直行
                elif Tracking_Left1Value == 1 and Tracking_Left2Value == 1 and Tracking_Right1Value == 1 and Tracking_Right2Value == 1:
                    car.Car_Run(30, 30)
                    time.sleep(1)
            
                nowTime = time.time()
#
            turnBack()
            return
        if cvResult == RED_YELLOW or cvResult == BLUE_GREEN or cvResult == RED_GREEN:
            turnBack()
            return
#
#
car.Car_Stop()
