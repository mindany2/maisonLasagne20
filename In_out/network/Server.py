import socket
import pickle
from tree.Tree import Tree
from threading import Thread
import io
import sys, traceback
from tree.utils.Logger import Logger

class Server:

    def __init__(self, getter, port = 5555):
        """
        This is a Server, it allows the client to send message to it
        and it just do that the message need to do and respond to the client
        """
        self.ip_address = socket.gethostbyname(socket.gethostname())
        self.port = port
        self.getter = getter
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.socket.bind(("", self.port))
        except socket.error as e:
            Logger.error(str(e))

        self.socket.listen(2)
        self.started = False

    def start(self):
        Logger.info("Waiting for a connection, Server Started")
        self.started = True
        while self.started:
            conn, addr = self.socket.accept()
            Logger.info("Connected to: "+ str(addr))
            process = Thread(target=self.threaded_client, args=[conn])
            process.start()

    def kill(self):
        self.started = False

    def threaded_client(self, conn):
        conn.send(pickle.dumps("hello"))
        while self.started:
            try:
                content = conn.recv(4096)
                if len(content) == 0:
                    continue
                requete = pickle.loads(content)
            except Exception as e: 
                Logger.error("Exception during request : "+str(e))
                break
            data = None
            if not requete:
                Logger.info(str(conn) + "is disconnect")
                break
            if requete == "kill me":
                Logger.info("demande de kill")
                data = pickle.dumps("ok")
                conn.send(pickle.dumps(len(data)))
                conn.send(data)
                break
            try:
                data = requete.do(self.getter)
            except Exception as e:
                Logger.error("Exception during requete : "+str(e))
                data = e

            try:
                byte_data = pickle.dumps(data)
                conn.send(pickle.dumps(len(byte_data)))
                conn.send(byte_data)
            except Exception as e:
                Logger.error("Exception during response send: ")
                Logger.error(e)
                break

        Logger.info("Lost connection")
        conn.close()

