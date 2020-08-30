import socketserver
import socket


class MyTCPHandler(socketserver.StreamRequestHandler):

    def handle(self):
        # self.rfile is a file-like object created by the handler;
        # we can now use e.g. readline() instead of raw recv() calls
        self.data = str(self.rfile.readline().strip(), "utf-8")
        print("{} wrote:".format(self.client_address[0]))
        print(self.data)
        
        
        # Likewise, self.wfile is a file-like object used to write back
        # to the client
        self.wfile.write(bytes(self.data.upper(), "utf-8"))

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

if __name__ == "__main__":
    HOST, PORT = get_ip(), 8000

    # Create the server, binding to localhost on port 9999
    with socketserver.TCPServer((HOST, PORT), MyTCPHandler) as server:
        # Activate the server; this will keep running until you
        # interrupt the program with Ctrl-C
        server.serve_forever()