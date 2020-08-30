import time
import threading
import socketserver
from PCA9685 import PCA9685
from time import ctime
import socket

host = '192.168.7.127'
port = 8000

def timerfunc():
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
    t = threading.Timer(0.02, timerfunc)
    t.start()


def process_request(request):
    print(request)
    return request
    
def start_servo():
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
    return pwm

def start_server():
    server_socket = socket.socket()  # get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))  # bind host address and port together

    # configure how many client the server can listen simultaneously
    server_socket.listen(2)
    conn, address = server_socket.accept()  # accept new connection
    print("Connection from: " + str(address))
    while True:
        # receive data stream. it won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        if not data:
            # if data is not received break
            break
        print("from connected user: " + str(data))
        data = input(' -> ')
        conn.send(data.encode())  # send data to the client

    conn.close()  # close the connection


t = threading.Timer(0.02, timerfunc)
t.setDaemon(True)
t.start()
pwm = start_servo()

start_server()

    