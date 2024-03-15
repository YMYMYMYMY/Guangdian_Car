import RPi.GPIO as GPIO
import serial
import time
# 串口设备名称
serial_port = '/dev/ttyACM0'

# 打开串口连接
ser = serial.Serial(serial_port, 115200)  # 根据需要设置波特率

#ser.open()
# 发送二进制代码
#binary_code = b'\x7B\x00\x00\x0F\x00\x00\x00\x00\x00\x74\x7D'  # 要发送的二进制代码

#ser.write(binary_code)


# 关闭串口连接


def runn(binary_code):
  ser = serial.Serial(serial_port, 115200)
  ser.write(binary_code)
  ser.close()

#binary_code_left = b'\x7B\x00\x00\x00\x00\x00\x00\x0F\x00\x74\x7D'


def run():
    ser = serial.Serial(serial_port, 115200)
    binary_code_run = b'\x7B\x00\x00\x0F\x00\x00\x00\x00\x00\x74\x7D'
    ser.write(binary_code_run)
    ser.close()
    return

def back():
    ser = serial.Serial(serial_port, 115200)
    binary_code_back = b'\x7B\x00\x00\xF1\x00\x00\x00\x00\x00\x8A\x7D'
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



#left()

#tingzzhi
#runn(b'\x7B\x00\x00\x00\x00\x00\x00\xF9\x00\x84\x7D')

#runn(b'\x7B\x00\x00\x00\x60\x00\x00\x00\x00\x1B\x7D')
#runn(b'\x7B\x00\x00\x00\x60\x00\x00\x00\x00\x1B\x7D')
#runn(b'\x7B\x00\x00\x00\x60\x00\x00\x00\x00\x1B\x7D')
left()
time.sleep(1.2)
stop()