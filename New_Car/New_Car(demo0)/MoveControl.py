#* coding:UTF8 *
import RPi.GPIO as GPIO
import serial
import time
import Distance
from JudgeTreasure import RED_GREEN, BLUE_YELLOW, BLUE_GREEN, RED_YELLOW
#

#
BLUE_YELLOW = 2  # 蓝色真
BLUE_GREEN = 4  # 蓝色假
RED_GREEN = 1  # 红色真
RED_YELLOW = 3  # 红色假



serial_port = '/dev/ttyACM0'

# 打开串口连接
ser = serial.Serial(serial_port, 115200)  # 根据需要设置波特率



Tracking_1 = 11
Tracking_2 = 13
Tracking_3 = 15
Tracking_4 = 29
Tracking_5 = 31
Tracking_6 = 33
Tracking_7 = 35
Tracking_8 = 37


#
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)


#
GPIO.setup(Tracking_1, GPIO.IN)
GPIO.setup(Tracking_2, GPIO.IN)
GPIO.setup(Tracking_3, GPIO.IN)
GPIO.setup(Tracking_4, GPIO.IN)
GPIO.setup(Tracking_5, GPIO.IN)
GPIO.setup(Tracking_6, GPIO.IN)
GPIO.setup(Tracking_7, GPIO.IN)
GPIO.setup(Tracking_8, GPIO.IN)
#
turnList = list()
accomplishTag = 1
#


def runn(binary_code):
  ser = serial.Serial(serial_port, 115200)
  ser.write(binary_code)
  ser.close()
  
def run():
    ser = serial.Serial(serial_port, 115200)
    #binary_code_run = b'\x7B\x00\x00\x0F\x00\x00\x00\x00\x00\x74\x7D'
    binary_code_run = b'\x7B\x00\x00\x02\x00\x00\x00\x00\x00\x79\x7D'
    ser.write(binary_code_run)
    ser.close()
    return

def back():
    ser = serial.Serial(serial_port, 115200)
    binary_code_back = b'\x7B\x00\x00\xFF\xB0\x00\x00\x00\x00\x34\x7D'
    ser.write(binary_code_back)
    ser.close()
    return

def stop():
    ser = serial.Serial(serial_port, 115200)
    binary_code_stop = b'\x7B\x00\x00\x00\x00\x00\x00\x00\x00\x7B\x7D'
    ser.write(binary_code_stop)
    ser.close()
    return

def left():
    ser = serial.Serial(serial_port, 115200)
    #binary_code_left = b'\x7B\x00\x00\x00\x00\x00\x00\x0F\x00\x74\x7D'
    binary_code_left = b'\x7B\x00\x00\x00\x00\x00\x00\x05\x00\x7E\x7D'
    #runn(b'\x7B\x00\x00\x00\x00\x00\x00\x03\x00\x78\x7D')
    #time.sleep(1.15)
    ser.write(binary_code_left)
    ser.close()
    return

def right():
    ser = serial.Serial(serial_port, 115200)
    #binary_code_left = b'\x7B\x00\x00\x00\x00\x00\x00\xF1\x00\x8A\x7D'
    binary_code_right = b'\x7B\x00\x00\x00\x00\x00\x00\xFB\x00\x80\x7D'
    ser.write(binary_code_right)
    ser.close()
    return

#
def distanceMove():
    distance = Distance.Distance()
    while distance > 13:
        tracking_function()
        distance = Distance.Distance()
    stop()
    time.sleep(2)
    return

 #遇到不是直行的路径，就来寻找方向指令，遇到转弯就回来查询转向，并按既定方向指令运动。
def move(orientList):
     #处理坐标，转化为控制
    global turnList, accomplishTag
    orientList.reverse()
    turnList = orientList
    stop()
    while accomplishTag:
        tracking_function()
    accomplishTag = 1
    distanceMove()
#
#
def goStraight():
    #电机驱动代码
    run()
    time.sleep(0.3)
#
#
def turnRight():
    #电机驱动代码
    run()
    time.sleep(0.15)
    right()
    time.sleep(0.4)
    while 1:
        right()
        Tracking_1Value = GPIO.input(Tracking_1)
        Tracking_2Value = GPIO.input(Tracking_2)
        Tracking_3Value = GPIO.input(Tracking_3)
        Tracking_4Value = GPIO.input(Tracking_4)
        Tracking_5Value = GPIO.input(Tracking_5)
        Tracking_6Value = GPIO.input(Tracking_6)
        Tracking_7Value = GPIO.input(Tracking_7)
        Tracking_8Value = GPIO.input(Tracking_8)
        #print(Tracking_Left1Value, Tracking_Left2Value, Tracking_Right1Value, Tracking_Right2Value)
        if Tracking_4Value == 0 or Tracking_5Value == 0:
            stop()
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
    run()
    time.sleep(0.15)
    left()
    time.sleep(0.4)
    while 1:
        left()
        Tracking_1Value = GPIO.input(Tracking_1)
        Tracking_2Value = GPIO.input(Tracking_2)
        Tracking_3Value = GPIO.input(Tracking_3)
        Tracking_4Value = GPIO.input(Tracking_4)
        Tracking_5Value = GPIO.input(Tracking_5)
        Tracking_6Value = GPIO.input(Tracking_6)
        Tracking_7Value = GPIO.input(Tracking_7)
        Tracking_8Value = GPIO.input(Tracking_8)
        #print(Tracking_Left1Value, Tracking_Left2Value, Tracking_Right1Value, Tracking_Right2Value)
        if Tracking_4Value == 0 or Tracking_5Value == 0:
            stop()
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
#def turnBack():
#    right()
#    time.sleep(0.6)
#    print("turn back")
#    while 1:
#        right()
#        time.sleep(0.02)
#        Tracking_1Value = GPIO.input(Tracking_1)
#        Tracking_2Value = GPIO.input(Tracking_2)
#        Tracking_3Value = GPIO.input(Tracking_3)
#        Tracking_4Value = GPIO.input(Tracking_4)
#        Tracking_5Value = GPIO.input(Tracking_5)
#        Tracking_6Value = GPIO.input(Tracking_6)
#        Tracking_7Value = GPIO.input(Tracking_7)
#        Tracking_8Value = GPIO.input(Tracking_8)
#        #print(Tracking_Left1Value, Tracking_Left2Value, Tracking_Right1Value, Tracking_Right2Value)
#        if Tracking_2Value == 0 or Tracking_3Value == 0:
#            #car.Car_Spin_Left(65, 65)
#            #time.sleep(0.2)
#            back()
#            time.sleep(0.8)
#            stop()
#            break
#
#
def turnBack():
    left()
    time.sleep(1.45)
    back()
    time.sleep(0.8)
    


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
    Tracking_1Value = GPIO.input(Tracking_1)
    Tracking_2Value = GPIO.input(Tracking_2)
    Tracking_3Value = GPIO.input(Tracking_3)
    Tracking_4Value = GPIO.input(Tracking_4)
    Tracking_5Value = GPIO.input(Tracking_5)
    Tracking_6Value = GPIO.input(Tracking_6)
    Tracking_7Value = GPIO.input(Tracking_7)
    Tracking_8Value = GPIO.input(Tracking_8)
#
    #print(Tracking_Left1Value, Tracking_Left2Value, Tracking_Right1Value, Tracking_Right2Value)
    #四路循迹引脚电平状态
    #1 0 0 0
    #1 1 0 0
    #处理右直角的转动
#1111 0000 and 1110 0000 and 1100 0000
    if (Tracking_1Value == 1 and Tracking_2Value == 1 and Tracking_3Value == 1 and Tracking_4Value == 1 and Tracking_5Value == 0 and Tracking_6Value == 0 and Tracking_7Value == 0 and Tracking_8Value == 0)or(Tracking_1Value == 1 and Tracking_2Value == 1 and Tracking_3Value == 0 and Tracking_4Value == 0 and Tracking_5Value == 0 and Tracking_6Value == 0 and Tracking_7Value == 0 and Tracking_8Value == 0)or(Tracking_1Value == 1 and Tracking_2Value == 1 and Tracking_3Value == 1 and Tracking_4Value == 0 and Tracking_5Value == 0 and Tracking_6Value == 0 and Tracking_7Value == 0 and Tracking_8Value == 0):
        print(Tracking_1Value,Tracking_2Value,Tracking_3Value,Tracking_4Value,Tracking_5Value,Tracking_6Value,Tracking_7Value,Tracking_8Value)
        where2Go()
#
    #四路循迹引脚电平状态
    #0 0 0 1
    #0 0 1 1
    #处理左直角的转动
    elif (Tracking_1Value == 0 and Tracking_2Value == 0 and Tracking_3Value == 0 and Tracking_4Value == 0 and Tracking_5Value == 1 and Tracking_6Value == 1 and Tracking_7Value == 1 and Tracking_8Value == 1)or(Tracking_1Value == 0 and Tracking_2Value == 0 and Tracking_3Value == 0 and Tracking_4Value == 0 and Tracking_5Value == 0 and Tracking_6Value == 1 and Tracking_7Value == 1 and Tracking_8Value == 1)or(Tracking_1Value == 0 and Tracking_2Value == 0 and Tracking_3Value == 0 and Tracking_4Value == 0 and Tracking_5Value == 0 and Tracking_6Value == 0 and Tracking_7Value == 1 and Tracking_8Value == 1):
        print(Tracking_1Value,Tracking_2Value,Tracking_3Value,Tracking_4Value,Tracking_5Value,Tracking_6Value,Tracking_7Value,Tracking_8Value)
        where2Go()
#
    #四路循迹引脚电平状态
    #0 0 0 0
    #处理丁字口的转动
    elif (Tracking_1Value == 0 and Tracking_2Value == 0 and Tracking_3Value == 0 and Tracking_4Value == 0 and Tracking_5Value == 0 and Tracking_6Value == 0 and Tracking_7Value == 0 and Tracking_8Value == 0):
        where2Go()
#
    #四路循迹引脚电平状态
    #1 0 1 1
    #0 1 1 1
    #处理左小弯
#1110 1111
    elif Tracking_1Value == 1 and Tracking_2Value == 1 and Tracking_3Value == 1 and Tracking_4Value == 0 and Tracking_5Value == 1 and Tracking_6Value == 1 and Tracking_7Value == 1 and Tracking_8Value == 1:
        print(Tracking_1Value,Tracking_2Value,Tracking_3Value,Tracking_4Value,Tracking_5Value,Tracking_6Value,Tracking_7Value,Tracking_8Value)
        runn(b'\x7B\x00\x00\x02\x00\x00\x00\x01\x00\x78\x7D')
        time.sleep(0.01)

#1101 1111
    elif Tracking_1Value == 1 and Tracking_2Value == 1 and Tracking_3Value == 0 and Tracking_4Value == 1 and Tracking_5Value == 1 and Tracking_6Value == 1 and Tracking_7Value == 1 and Tracking_8Value == 1:
        print(Tracking_1Value,Tracking_2Value,Tracking_3Value,Tracking_4Value,Tracking_5Value,Tracking_6Value,Tracking_7Value,Tracking_8Value)
        runn(b'\x7B\x00\x00\x02\x00\x00\x00\x02\x00\x7B\x7D')
        time.sleep(0.01)

#1011 1111
    elif Tracking_1Value == 1 and Tracking_2Value == 0 and Tracking_3Value == 1 and Tracking_4Value == 1 and Tracking_5Value == 1 and Tracking_6Value == 1 and Tracking_7Value == 1 and Tracking_8Value == 1:
        print(Tracking_1Value,Tracking_2Value,Tracking_3Value,Tracking_4Value,Tracking_5Value,Tracking_6Value,Tracking_7Value,Tracking_8Value)
        runn(b'\x7B\x00\x00\x02\x00\x00\x00\x03\x00\x7A\x7D')
        time.sleep(0.01)

#1100 1111
    elif Tracking_1Value == 1 and Tracking_2Value == 1 and Tracking_3Value == 0 and Tracking_4Value == 0 and Tracking_5Value == 1 and Tracking_6Value == 1 and Tracking_7Value == 1 and Tracking_8Value == 1:
        print(Tracking_1Value,Tracking_2Value,Tracking_3Value,Tracking_4Value,Tracking_5Value,Tracking_6Value,Tracking_7Value,Tracking_8Value)
        runn(b'\x7B\x00\x00\x02\x00\x00\x00\x02\x00\x7B\x7D')
        time.sleep(0.01)
        
#1001 1111
    elif Tracking_1Value == 1 and Tracking_2Value == 0 and Tracking_3Value == 0 and Tracking_4Value == 1 and Tracking_5Value == 1 and Tracking_6Value == 1 and Tracking_7Value == 1 and Tracking_8Value == 1:
        print(Tracking_1Value,Tracking_2Value,Tracking_3Value,Tracking_4Value,Tracking_5Value,Tracking_6Value,Tracking_7Value,Tracking_8Value)
        runn(b'\x7B\x00\x00\x02\x00\x00\x00\x03\x00\x7A\x7D')
        time.sleep(0.01)
#0011 1111
    elif Tracking_1Value == 0 and Tracking_2Value == 0 and Tracking_3Value == 1 and Tracking_4Value == 1 and Tracking_5Value == 1 and Tracking_6Value == 1 and Tracking_7Value == 1 and Tracking_8Value == 1:
        print(Tracking_1Value,Tracking_2Value,Tracking_3Value,Tracking_4Value,Tracking_5Value,Tracking_6Value,Tracking_7Value,Tracking_8Value)
        runn(b'\x7B\x00\x00\x02\x00\x00\x00\x04\x00\x7D\x7D')
        time.sleep(0.01)
#0111 1111
    elif Tracking_1Value == 0 and Tracking_2Value == 1 and Tracking_3Value == 1 and Tracking_4Value == 1 and Tracking_5Value == 1 and Tracking_6Value == 1 and Tracking_7Value == 1 and Tracking_8Value == 1:
        print(Tracking_1Value,Tracking_2Value,Tracking_3Value,Tracking_4Value,Tracking_5Value,Tracking_6Value,Tracking_7Value,Tracking_8Value)
        runn(b'\x7B\x00\x00\x02\x00\x00\x00\x05\x00\x7C\x7D')
        time.sleep(0.01)
#1100 0111        
    elif Tracking_1Value == 1 and Tracking_2Value == 1 and Tracking_3Value == 0 and Tracking_4Value == 0 and Tracking_5Value == 0 and Tracking_6Value == 1 and Tracking_7Value == 1 and Tracking_8Value == 1:
        print(Tracking_1Value,Tracking_2Value,Tracking_3Value,Tracking_4Value,Tracking_5Value,Tracking_6Value,Tracking_7Value,Tracking_8Value)
        runn(b'\x7B\x00\x00\x02\x00\x00\x00\x01\x00\x78\x7D')
        time.sleep(0.01)
#1000 1111        
    elif Tracking_1Value == 1 and Tracking_2Value == 0 and Tracking_3Value == 0 and Tracking_4Value == 0 and Tracking_5Value == 1 and Tracking_6Value == 1 and Tracking_7Value == 1 and Tracking_8Value == 1:
        print(Tracking_1Value,Tracking_2Value,Tracking_3Value,Tracking_4Value,Tracking_5Value,Tracking_6Value,Tracking_7Value,Tracking_8Value)
        runn(b'\x7B\x00\x00\x02\x00\x00\x00\x01\x00\x78\x7D')
        time.sleep(0.01)
        
#chuliyouxiaowan
#1111 0111

    elif Tracking_1Value == 1 and Tracking_2Value == 1 and Tracking_3Value == 1 and Tracking_4Value == 1 and Tracking_5Value == 0 and Tracking_6Value == 1 and Tracking_7Value == 1 and Tracking_8Value == 1:
        print(Tracking_1Value,Tracking_2Value,Tracking_3Value,Tracking_4Value,Tracking_5Value,Tracking_6Value,Tracking_7Value,Tracking_8Value)
        runn(b'\x7B\x00\x00\x02\x00\x00\x00\xFF\x00\x86\x7D')
        time.sleep(0.01)

#1111 1011
    elif Tracking_1Value == 1 and Tracking_2Value == 1 and Tracking_3Value == 1 and Tracking_4Value == 1 and Tracking_5Value == 1 and Tracking_6Value == 0 and Tracking_7Value == 1 and Tracking_8Value == 1:
        print(Tracking_1Value,Tracking_2Value,Tracking_3Value,Tracking_4Value,Tracking_5Value,Tracking_6Value,Tracking_7Value,Tracking_8Value)
        runn(b'\x7B\x00\x00\x02\x00\x00\x00\xFE\x00\x87\x7D')
        time.sleep(0.01)

#1111 1101
    elif Tracking_1Value == 1 and Tracking_2Value == 1 and Tracking_3Value == 1 and Tracking_4Value == 1 and Tracking_5Value == 1 and Tracking_6Value == 1 and Tracking_7Value == 0 and Tracking_8Value == 1:
        print(Tracking_1Value,Tracking_2Value,Tracking_3Value,Tracking_4Value,Tracking_5Value,Tracking_6Value,Tracking_7Value,Tracking_8Value)
        runn(b'\x7B\x00\x00\x02\x00\x00\x00\xFC\x00\x85\x7D')
        time.sleep(0.01)

#1111 0011
    elif Tracking_1Value == 1 and Tracking_2Value == 1 and Tracking_3Value == 1 and Tracking_4Value == 1 and Tracking_5Value == 0 and Tracking_6Value == 0 and Tracking_7Value == 1 and Tracking_8Value == 1:
        print(Tracking_1Value,Tracking_2Value,Tracking_3Value,Tracking_4Value,Tracking_5Value,Tracking_6Value,Tracking_7Value,Tracking_8Value)
        runn(b'\x7B\x00\x00\x02\x00\x00\x00\xFE\x00\x87\x7D')
        time.sleep(0.01)
        
#1111 1001
    elif Tracking_1Value == 1 and Tracking_2Value == 1 and Tracking_3Value == 1 and Tracking_4Value == 1 and Tracking_5Value == 1 and Tracking_6Value == 0 and Tracking_7Value == 0 and Tracking_8Value == 1:
        print(Tracking_1Value,Tracking_2Value,Tracking_3Value,Tracking_4Value,Tracking_5Value,Tracking_6Value,Tracking_7Value,Tracking_8Value)
        runn(b'\x7B\x00\x00\x02\x00\x00\x00\xFD\x00\x84\x7D')
        time.sleep(0.01)
#1111 1100
    elif Tracking_1Value == 1 and Tracking_2Value == 1 and Tracking_3Value == 1 and Tracking_4Value == 1 and Tracking_5Value == 1 and Tracking_6Value == 1 and Tracking_7Value == 0 and Tracking_8Value == 0:
        print(Tracking_1Value,Tracking_2Value,Tracking_3Value,Tracking_4Value,Tracking_5Value,Tracking_6Value,Tracking_7Value,Tracking_8Value)
        runn(b'\x7B\x00\x00\x02\x00\x00\x00\xFC\x00\x85\x7D')
        time.sleep(0.01)
#1111 1110
    elif Tracking_1Value == 1 and Tracking_2Value == 1 and Tracking_3Value == 1 and Tracking_4Value == 1 and Tracking_5Value == 1 and Tracking_6Value == 1 and Tracking_7Value == 1 and Tracking_8Value == 0:
        print(Tracking_1Value,Tracking_2Value,Tracking_3Value,Tracking_4Value,Tracking_5Value,Tracking_6Value,Tracking_7Value,Tracking_8Value)
        runn(b'\x7B\x00\x00\x02\x00\x00\x00\xFB\x00\x82\x7D')
        time.sleep(0.01)
#1110 0011        
    elif Tracking_1Value == 1 and Tracking_2Value == 1 and Tracking_3Value == 1 and Tracking_4Value == 0 and Tracking_5Value == 0 and Tracking_6Value == 0 and Tracking_7Value == 1 and Tracking_8Value == 1:
        print(Tracking_1Value,Tracking_2Value,Tracking_3Value,Tracking_4Value,Tracking_5Value,Tracking_6Value,Tracking_7Value,Tracking_8Value)
        runn(b'\x7B\x00\x00\x02\x00\x00\x00\xFF\x00\x86\x7D')
        time.sleep(0.01)
#1111 0001        
    elif Tracking_1Value == 1 and Tracking_2Value == 1 and Tracking_3Value == 1 and Tracking_4Value == 1 and Tracking_5Value == 0 and Tracking_6Value == 0 and Tracking_7Value == 0 and Tracking_8Value == 1:
        print(Tracking_1Value,Tracking_2Value,Tracking_3Value,Tracking_4Value,Tracking_5Value,Tracking_6Value,Tracking_7Value,Tracking_8Value)
        runn(b'\x7B\x00\x00\x02\x00\x00\x00\xFF\x00\x86\x7D')
        time.sleep(0.01)

#
    #四路循迹引脚电平状态
    #1 0 0 1
    #处理直线
    if Tracking_1Value == 1 and Tracking_2Value == 1 and Tracking_3Value == 1 and Tracking_4Value == 0 and Tracking_5Value == 0 and Tracking_6Value == 1 and Tracking_7Value == 1 and Tracking_8Value == 1:
        print(Tracking_1Value,Tracking_2Value,Tracking_3Value,Tracking_4Value,Tracking_5Value,Tracking_6Value,Tracking_7Value,Tracking_8Value)
        run()
        time.sleep(0.01)
#
    #当为1 1 1 1时小车直行
    elif Tracking_1Value == 1 and Tracking_2Value == 1 and Tracking_3Value == 1 and Tracking_4Value == 0 and Tracking_5Value == 0 and Tracking_6Value == 1 and Tracking_7Value == 1 and Tracking_8Value == 1:
        print(Tracking_1Value,Tracking_2Value,Tracking_3Value,Tracking_4Value,Tracking_5Value,Tracking_6Value,Tracking_7Value,Tracking_8Value)
        run()
        time.sleep(0.01)
    
#







def cvResultMove(cvResult, teamColor):
    if teamColor == 1:
        if cvResult == RED_GREEN:
            beginTime = time.time()
            nowTime = time.time()
#
            while nowTime - beginTime < 0.8:
                Tracking_1Value = GPIO.input(Tracking_1)
                Tracking_2Value = GPIO.input(Tracking_2)
                Tracking_3Value = GPIO.input(Tracking_3)
                Tracking_4Value = GPIO.input(Tracking_4)
                Tracking_5Value = GPIO.input(Tracking_5)
                Tracking_6Value = GPIO.input(Tracking_6)
                Tracking_7Value = GPIO.input(Tracking_7)
                Tracking_8Value = GPIO.input(Tracking_8)
                #print("imhere")
                if Tracking_1Value == 1 and Tracking_2Value == 1 and Tracking_3Value == 1 and Tracking_4Value == 0 and Tracking_5Value == 0 and Tracking_6Value == 1 and Tracking_7Value == 1 and Tracking_8Value == 1:
                    print(Tracking_1Value,Tracking_2Value,Tracking_3Value,Tracking_4Value,Tracking_5Value,Tracking_6Value,Tracking_7Value,Tracking_8Value)
                    run()
                    #print("1001lo")
                    time.sleep(0.01)
                   
#
                    #当为1 1 1 1时小车直行
                elif Tracking_1Value == 1 and Tracking_2Value == 1 and Tracking_3Value == 1 and Tracking_4Value == 1 and Tracking_5Value == 1 and Tracking_6Value == 1 and Tracking_7Value == 1 and Tracking_8Value == 1:
                    runn(b'\x7B\x00\x00\x00\x60\x00\x00\x00\x00\x1B\x7D')
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
                Tracking_1Value = GPIO.input(Tracking_1)
                Tracking_2Value = GPIO.input(Tracking_2)
                Tracking_3Value = GPIO.input(Tracking_3)
                Tracking_4Value = GPIO.input(Tracking_4)
                Tracking_5Value = GPIO.input(Tracking_5)
                Tracking_6Value = GPIO.input(Tracking_6)
                Tracking_7Value = GPIO.input(Tracking_7)
                Tracking_8Value = GPIO.input(Tracking_8)
                if Tracking_1Value == 1 and Tracking_2Value == 1 and Tracking_3Value == 1 and Tracking_4Value == 0 and Tracking_5Value == 0 and Tracking_6Value == 1 and Tracking_7Value == 1 and Tracking_8Value == 1:
                    print(Tracking_1Value,Tracking_2Value,Tracking_3Value,Tracking_4Value,Tracking_5Value,Tracking_6Value,Tracking_7Value,Tracking_8Value)
                    run()
                    time.sleep(0.01)
#
                    #当为1 1 1 1时小车直行
                elif Tracking_1Value == 1 and Tracking_2Value == 1 and Tracking_3Value == 1 and Tracking_4Value == 1 and Tracking_5Value == 1 and Tracking_6Value == 1 and Tracking_7Value == 1 and Tracking_8Value == 1:
                    runn(b'\x7B\x00\x00\x00\x60\x00\x00\x00\x00\x1B\x7D')
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
stop()

