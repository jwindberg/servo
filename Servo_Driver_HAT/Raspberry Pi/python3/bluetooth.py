#!/usr/bin/python
# -*- coding:utf-8 -*-
import os
import serial
import time
from PCA9685 import PCA9685
import subprocess
import threading

pwm = PCA9685(0x40)
pwm.set_pwm_freq(50)

pos0 = 1500
pos1 = 1500
pos2 = 1500
pos3 = 1500
step0 = 0
step1 = 0
step2 = 0
step3 = 0
pwm.set_servo_pulse(0, pos0)
pwm.set_servo_pulse(1, pos1)
pwm.set_servo_pulse(2, pos2)
pwm.set_servo_pulse(3, pos3)

# os.system("echo \"discoverable on\" | bluetoothctl")
bt = serial.Serial("/dev/rfcomm0", 115200)
print('serial test start ...')
bt.flushInput()


def timer_func():
    global step0, step1, step2, step3, pos0, pos1, pos2, pos3, pwm

    if step0 != 0:
        pos0 += step0
        if pos0 >= 2500:
            pos0 = 2500
        if pos0 <= 500:
            pos0 = 500
        # set channel 0
        pwm.set_servo_pulse(0, pos0)

    if step1 != 0:
        pos1 += step1
        if pos1 >= 2500:
            pos1 = 2500
        if pos1 <= 500:
            pos1 = 500
        # set channel 1
        pwm.set_servo_pulse(1, pos1)

    if step2 != 0:
        pos2 += step2
        if pos2 >= 2500:
            pos2 = 2500
        if pos2 <= 500:
            pos2 = 500
        # set channel 2
        pwm.set_servo_pulse(2, pos2)

    if step3 != 0:
        pos3 += step3
        if pos3 >= 2500:
            pos3 = 2500
        if pos3 <= 500:
            pos3 = 500
        # set channel 3
        pwm.set_servo_pulse(3, pos3)

    global t  # Notice: use global variable!
    t = threading.Timer(0.02, timer_func)
    t.start()


t = threading.Timer(0.02, timer_func)
t.setDaemon(True)
t.start()

try:
    while True:
        data = ""
        while bt.inWaiting() > 0:
            data += bt.read(bt.inWaiting()).decode('utf-8')
        if data != "":
            print(data)
            if not data:
                break
            if data == "Stop":
                step0 = 0
                step1 = 0
                step2 = 0
                step3 = 0
                print("1")
            elif data == "Forward":
                step0 = -5
                print("2")
            elif data == "Backward":
                step0 = 5
                print("3")
            elif data == "TurnLeft":
                step1 = -5
                print("4")
            elif data == "TurnRight":
                step1 = 5
                print("5")
            elif data == "Up":
                step2 = -5
                print("6")
            elif data == "Down":
                step2 = 5
                print("7")
            elif data == "Left":
                step3 = 5
                print("8")
            elif data == "Right":
                step3 = -5
                print("9")
        time.sleep(0.0001)
except KeyboardInterrupt:
    if bt is not None:
        bt.close()
