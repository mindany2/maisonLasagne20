import unittest
from tree.Mode import Mode
from unittest.mock import Mock, MagicMock
from mock import patch
import threading
from time import sleep
import pytest
from parametrize import parametrize
from In_out.network.Client import Client
from In_out.network.Server import Server
from In_out.network.messages.get.Get_tree_infos import Get_tree_infos

class TestClientServer(unittest.TestCase):

    def start(self):
        self.getter = MagicMock()
        self.server = Server(self.getter)
        self.client = Client()

        threading.Thread(target=self.server.start).start()


    def kill(self):
        self.server.kill()

    def test_start(self):
        self.start()
        sleep(0.1)
        self.assertTrue(self.server.started)
        
        self.client.start()

        respond = self.client.send(Get_tree_infos())

        self.assertEqual(respond, str(self.getter.get_tree()))

        self.client.disconnect()

        self.kill()




        

 
