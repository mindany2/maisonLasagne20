import socket
import pickle
from tree.Tree import Tree
from threading import Thread
import io

server = "192.168.1.13"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

class StrToBytes:
    def __init__(self, fileobj):
        self.fileobj = fileobj
    def read(self, size):
        return self.fileobj.read(size).encode()
    def readline(self, size=-1):
        return self.fileobj.readline(size).encode()
 


def pickle_tree():
    liste_env = Tree().liste_envi
    print(liste_env)
    reply = pickle.dumps(liste_env)
    return reply

def threaded_client(conn):
    conn.send(pickle_tree())
    while True:
        try:
            data = pickle.loads(conn.recv(2048))
            # data est un ordre, une fonction à éxécuter
            if not data:
                print("Disconnected")
                break
            else:
                # traitement de l'ordre

                print("Received: ", data)

            conn.sendall(pickle.dumps(Tree(),protocol=0))
        except:
            break

    print("Lost connection")
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    threaded_client(conn)
