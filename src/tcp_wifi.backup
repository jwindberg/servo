import time
import threading
import socketserver
from PCA9685 import PCA9685
from time import ctime
import socket


class RequestHandler(socketserver.StreamRequestHandler):
    def handle(self):
        global step0, step1, step2, step3
        print('got connection from ', self.client_address)
        self.wfile.write(bytes(('connection %s:%s at %s succeed!' % (host, str, ctime())), "utf-8"))
        while True:
            data = str(self.rfile.readline().strip(), "utf-8")
            print("in-> " + data)
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
            print("out-> " + data)
            self.wfile.write(bytes(data + "\n", "utf-8"))

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except Exception:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP


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

host = get_ip()
port = 8000
print(host + ':%d' % port)
addr = (host, port)
t = threading.Timer(0.02, timerfunc)
t.setDaemon(True)
t.start()

server = socketserver.ThreadingTCPServer(addr, RequestHandler)
print('server is running....')
server.serve_forever()
