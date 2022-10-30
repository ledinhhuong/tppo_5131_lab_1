import json
import socket
from threading import Lock
import os
import threading
import argparse

parser = argparse.ArgumentParser(description='Ip and port of Server')
parser.add_argument('server_ip', type=str, help='Ip of Server')
parser.add_argument('server_port', type=int, help='Port of Server')
args = parser.parse_args()

def read_txt():
    path = 'blinds.txt'
    with open(path, 'r') as file:
        data = file.readlines()
    shear_percent = int(data[0].split()[-1])
    flux_percent = int(data[1].split()[-1])
    current_illumination  = int(data[2].split()[-1])
    vals = [shear_percent, flux_percent, current_illumination]
    return vals

def write_txt(data):
    path = 'blinds.txt'
    with open(path, 'w') as file:
        file.write(data)

vals = read_txt()

parameters = ['shaer', 'flux', 'illumination']

class Server: 
    def __init__(self, host, port):
        self.sock = self._setup_socket(host,port)
        self.connections = []
        print("[STARTING] Server is listening on {}: {}".format(host, port))

    def run(self):
        blinds_changes_thread = threading.Thread(target=self.blinds_changes)
        blinds_changes_thread.daemon = True
        blinds_changes_thread.start()
           
        while(True):
            conn, addr = self.sock.accept()
            if (self._check_for_existing_conn(conn) == False):
                self.connections.append(conn)
            else:
                print("Connection has already existed")
            print(f"[NEW CONNECTION] {addr} connected")

            cmd_parsing_thread = threading.Thread(target=self.cmd_parsing,args=(conn, addr))

            cmd_parsing_thread.daemon = True
            cmd_parsing_thread.start()   
        

    def blinds_changes(self):
        deviceFileName = 'blinds.txt'
        _cached_stamp = os.stat(deviceFileName).st_mtime
        while (True):
            stamp = os.stat(deviceFileName).st_mtime
            if(stamp != _cached_stamp):
                _cached_stamp = stamp

                new_vals = read_txt()

                for idx in range(3):

                    if new_vals[idx] != vals[idx]:
                        for connection in self.connections:
                            connection.send('{} has been changed to {}'.format(parameters[idx], new_vals[idx]).encode())
                        vals[idx] = new_vals[idx]
                        

    def cmd_parsing(self, conn, addr):
        while(True):
            byteData = conn.recv(4096)
            stringData = byteData.decode("utf-8")
            print('CLIENT: ', stringData)
            f_json = json.loads(stringData)
            vals = read_txt()
            if f_json['command']=='set':
                idx = ['shaer', 'flux', 'illumination'].index(f_json['parameter'])
                vals[idx] = f_json['value']
                
                data = 'shear_percent {}\nflux_percent {}\ncurrent_illumination {}\n'.format(vals[0], vals[1], vals[2])
                write_txt(data)
            
            if f_json['command']=='get':
                idx = ['shaer', 'flux', 'illumination'].index(f_json['parameter'])
                conn.send("{}: {}".format(f_json['parameter'], vals[idx]).encode())
    
    def _check_for_existing_conn(self, conn):
        connExists = False
        for connection in self.connections:
            if (str(conn) == str(connection)):
                connExists = True
                break
        return connExists

    @staticmethod
    def _setup_socket(host,port):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((host, port))
        sock.listen()
        return sock


if __name__ == "__main__":
    server = Server(args.server_ip, args.server_port)
    server.run()