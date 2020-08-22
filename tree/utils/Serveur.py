import socket
import pickle
from tree.Tree import Tree
from threading import Thread
import io
import sys, traceback
import netifaces as ni
from utils.Logger import Logger

"""
Ceci est le serveur de socket, il permet à tous les périphériques clients
de se connecté et d'avoir accès à l'arbre
"""

ni.ifaddresses('eth0')
ip_address = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']

port = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((ip_address, port))
except socket.error as e:
    str(e)

s.listen(2)
Logger.info("Waiting for a connection, Server Started")

def threaded_client(conn):
    conn.send(pickle.dumps("hello"))
    while True:
        try:
            requete = pickle.loads(conn.recv(2048))
            # requete est un ordre, une fonction à éxécuter
            data = None
            if not requete:
                Logger.info(str(conn) + "is disconnect")
                break
            try:
                data = requete.do()
                Logger.debug(data)
            except e:
                Logger.error("Exception during client message: ")
                Logger.error(e)
                break
            conn.send(pickle.dumps(data))
        except:
            break

    Logger.info("Lost connection")
    conn.close()

while True:
    conn, addr = s.accept()
    Logger.info("Connected to: "+ str(addr))
    process = Thread(target=threaded_client, args=[conn])
    process.start()
