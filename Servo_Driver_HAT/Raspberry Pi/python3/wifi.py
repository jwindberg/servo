import time
import threading
import socketserver
from PCA9685 import PCA9685
from time import ctime
import socket

print("start")

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

time.sleep(5)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(('8.8.8.8', 80))
host = s.getsockname()[0]
port = 8000
print(host + ':%d' % port)
addr = (host, port)


class Servers(socketserver.StreamRequestHandler):
    def handle(self):
        global step0, step1, step2, step3
        print('got connection from ', self.client_address)
        self.wfile.write(('connection %s:%s at %s succeed!' % (host, str, ctime())).encode('utf-8'))
        while True:
            data = self.request.recv(1024)
            data = data.decode('utf-8')
            if not data:
                break
            if data == "Stop":
                step0 = 0
                step1 = 0
                step2 = 0
                step3 = 0
            elif data == "Forward":
                step0 = -5
            elif data == "Backward":
                step0 = 5
            elif data == "TurnLeft":
                step1 = -5
            elif data == "TurnRight":
                step1 = 5
            elif data == "Up":
                step2 = -5
            elif data == "Down":
                step2 = 5
            elif data == "Left":
                step3 = 5
            elif data == "Right":
                step3 = -5
            print(data)
            # print "recv from ", self.client_address[0]
            self.request.send(data.encode('utf-8'))


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


t = threading.Timer(0.02, timerfunc)
t.setDaemon(True)
t.start()

server = socketserver.ThreadingTCPServer(addr, Servers)
print('server is running....')
server.serve_forever()
