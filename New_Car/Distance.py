#用于在树莓派上使用超声波传感器测量距
#离的Python代码。它使用RPi.GPIO库来控制树莓派的GPIO引脚，以便触发超声波测距模块并接收回波以计算距离。
#导入必要的库和模块：
#RPi.GPIO：用于树莓派的GPIO控制库。
#time：用于处理时间的标准Python库。
#设置GPIO编码方式和GPIO口的初始化：
#EchoPin和TrigPin变量定义了超声波传感器的回波引脚和触发引脚的引脚编号。
#GPIO.setmode(GPIO.BOARD)将GPIO口的编码方式设置为BOARD，这表示你将使用物理引脚编号来引用GPIO口。
#设置GPIO口的工作模式：
#GPIO.setup(EchoPin, GPIO.IN)将EchoPin设置为输入模式，用于接收超声波的回波信号。
#GPIO.setup(TrigPin, GPIO.OUT)将TrigPin设置为输出模式，用于触发超声波传感器。
#Distance函数：
#这是测量距离的主要功能。它通过发出一个短脉冲来触发超声波传感器，然后计算回波的时间来估算距离。函数返回距离的值（单位：厘米）。
#Distance_test函数：
#这个函数执行了多次测量，并返回多次测量的平均值。
#循环5次测量，排除了可能的异常值。
#计算并返回三次有效测量的平均距离值。

# -*- coding:UTF-8 -*-
import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)

EchoPin = 18
TrigPin = 16

# 设置GPIO口为BCM编码方式
GPIO.setmode(GPIO.BOARD)

GPIO.setup(EchoPin, GPIO.IN)
GPIO.setup(TrigPin, GPIO.OUT)


# 超声波函数
def Distance():
    GPIO.output(TrigPin, GPIO.LOW)
    time.sleep(0.000002)
    GPIO.output(TrigPin, GPIO.HIGH)
    time.sleep(0.000015)
    GPIO.output(TrigPin, GPIO.LOW)

    t3 = time.time()

    while not GPIO.input(EchoPin):
        t4 = time.time()
        if (t4 - t3) > 0.03:
            return -1
    t1 = time.time()
    while GPIO.input(EchoPin):
        t5 = time.time()
        if (t5 - t1) > 0.03:
            return -1

    t2 = time.time()
    time.sleep(0.01)
    print ("distance_1 is %d " % (((t2 - t1)* 340 / 2) * 100))
    return ((t2 - t1) * 340 / 2) * 100


def Distance_test():
    num = 0
    ultrasonic = []
    while num < 5:
        distance = Distance()
        # print("distance is %f"%(distance) )
        while int(distance) == -1:
            distance = Distance()
            # print("Tdistance is %f"%(distance) )
        while int(distance) >= 500 or int(distance) == 0:
            distance = Distance()
            # print("Edistance is %f"%(distance) )
        ultrasonic.append(distance)
        num = num + 1
        time.sleep(0.01)
    distance = (ultrasonic[1] + ultrasonic[2] + ultrasonic[3]) / 3
    print("distance is %f" % distance)
    return distance
#Distance_test()