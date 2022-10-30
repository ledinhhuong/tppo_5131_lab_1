import socket
from threading import Thread
import json
import argparse

parser = argparse.ArgumentParser(description='Ip and port of Server')
parser.add_argument('server_ip', type=str, help='Ip of Server')
parser.add_argument('server_port', type=int, help='Port of Server')
args = parser.parse_args()

class Client:
    def __init__(self, host, port):
        self.sock = self._setup_socket(host, port)
        thread = Thread(target=self.send_cmd)
        thread.daemon = True
        thread.start()

        print("[CONNECTED] Client connected to server at {}: {}".format(host, port))
        print("Parameters: shaer (0..100); flux (0..100); illumination (0..5000)")
        print("Syntax:\n\
    get <parameter>\n\
    set <parameter> <value>")
        while(True):
            data = self.sock.recv(4096)
            print("SERVER: ", data.decode())

    def send_cmd(self):
        while(True):
            try:
                text = input()
                elements = text.split()
                parameters = ['shaer', 'flux', 'illumination']
                if len(elements)==3 and elements[0]=='set' and elements[1] in parameters[0:2] and 0<=float(elements[2])<=100:
                    set_json = {
                        'command' : elements[0],
                        'parameter' : elements[1],
                        'value' : elements[2]    
                            }
                    self.sock.send(json.dumps(set_json).encode('utf-8'))
                elif len(elements)==2 and elements[0]=='get' and elements[1] in parameters:
                    get_json = {
                        'command' : elements[0],
                        'parameter' : elements[1],
                        }
                    self.sock.send(json.dumps(get_json).encode('utf-8'))
                else:
                    print('Syntax error')
            except:
                print('Syntax error')

    @staticmethod
    def _setup_socket(host, port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))
        return sock

if __name__ == "__main__":
    client = Client(args.server_ip, args.server_port)