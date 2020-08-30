import time
import threading
import socketserver
from socketserver import ThreadingTCPServer, StreamRequestHandler
from PCA9685 import PCA9685
from time import ctime
import socket

class Servo():
    def __init__(self):
        self.pos0 = 1500
        self.pos1 = 1500
        self.pos2 = 1500
        self.pos3 = 1500
        self.step0 = 0
        self.step1 = 0
        self.step2 = 0
        self.step3 = 0
        
        self.pwm = PCA9685(0x40)
        self.pwm.set_pwm_freq(50)

        self.pwm.set_servo_pulse(0, self.pos0)
        self.pwm.set_servo_pulse(1, self.pos1)
        self.pwm.set_servo_pulse(2, self.pos2)
        self.pwm.set_servo_pulse(3, self.pos3)
        
        self.timer = threading.Timer(0.02, self.timer_callback)
        self.timer.setDaemon(True)
        self.timer.start()
    
    def timer_callback(self):
        if self.step0 != 0:
            self.pos0 += self.step0
            if self.pos0 >= 2500:
                self.pos0 = 2500
            if self.pos0 <= 500:
                self.pos0 = 500
            # set channel 0
            self.pwm.set_servo_pulse(0, self.pos0)

        if self.step1 != 0:
            self.pos1 += self.step1
            if self.pos1 >= 2500:
                self.pos1 = 2500
            if self.pos1 <= 500:
                self.pos1 = 500
            # set channel 1
            self.pwm.set_servo_pulse(1, self.pos1)

        if self.step2 != 0:
            self.pos2 += self.step2
            if self.pos2 >= 2500:
                self.pos2 = 2500
            if self.pos2 <= 500:
                self.pos2 = 500
            # set channel 2
            self.pwm.set_servo_pulse(2, self.pos2)

        if self.step3 != 0:
            self.pos3 += self.step3
            if self.pos3 >= 2500:
                self.pos3 = 2500
            if self.pos3 <= 500:
                self.pos3 = 500
            # set channel 3
            self.pwm.set_servo_pulse(3, self.pos3)

        self.timer = threading.Timer(0.02, self.timer_callback)
        self.timer.start()
        
    def handle(self, data):
        if data == "Stop":
            self.step0 = 0
            self.step1 = 0
            self.step2 = 0
            self.step3 = 0
        elif data == "Forward":
            self.step0 = -5
        elif data == "Backward":
            self.step0 = 5
        elif data == "TurnLeft":
            self.step1 = -5
        elif data == "TurnRight":
            self.step1 = 5
        elif data == "Up":
            self.step2 = -5
        elif data == "Down":
            self.step2 = 5
        elif data == "Left":
            self.step3 = 5
        elif data == "Right":
            self.step3 = -5
            

class RequestHandler(StreamRequestHandler):
    def __init__(self, ip, servo):
        self.ip = ip
        self.servo = servo
        
    def handle(self):
        global step0, step1, step2, step3
        print('got connection from ', self.client_address)
        self.wfile.write(bytes(('connection %s:%s at %s succeed!' % (self.ip, str, ctime())), "utf-8"))
        while True:
            data = str(self.rfile.readline().strip(), "utf-8")
            print("in-> " + data)
            if not data:
                break
            servo.handle(data)
            print("out-> " + data)
            self.wfile.write(bytes(data + "\n", "utf-8"))
    
    def __call__(self, request, client_address, server):
        handler = RequestHandler(self.ip, self.servo)
        StreamRequestHandler.__init__(handler, request, client_address, server)

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


if __name__ == '__main__':

    servo = Servo()

    ip = get_ip()
    port = 8000
    addr = (ip, port)

    server = ThreadingTCPServer(addr, RequestHandler(ip, servo))
    print('server is running (%s:%d)' % addr)
    server.serve_forever()
