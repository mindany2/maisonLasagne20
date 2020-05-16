import socket
import pickle
from tree.Tree import Tree
from threading import Thread
import io
import sys

"""
Ceci est le serveur de socket, il permet à tous les périphériques clients
de se connecté et d'avoir accès à l'arbre
"""

server = "192.168.1.13"
port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((server, port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, Server Started")

def threaded_client(conn):
    conn.send(pickle.dumps("hello"))
    while True:
        try:
            requete = pickle.loads(conn.recv(2048))
            # requete est un ordre, une fonction à éxécuter
            data = None
            if not requete:
                print("Disconnected")
                break
            else:
                # traitement de l'ordre de la forme "fonction(arg1, arg2)"
                print("Received: ", requete)
                try:
                    data = eval("Tree()."+requete)
                    print(data)
                except:
                    print("Unexpected error:", sys.exc_info()[0])
                    data = "Error:la methodes ou les arguments ne sont pas valide \n on veut la forme \"fonction(arg1, arg2)\""
            print("pickeled = ", len(pickle.dumps(data)))
            conn.send(pickle.dumps(data))
        except:
            break

    print("Lost connection")
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to:", addr)
    process = Thread(target=threaded_client, args=[conn])
    process.start()
