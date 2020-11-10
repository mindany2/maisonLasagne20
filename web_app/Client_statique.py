from utils.communication.Client import Client
from utils.communication.get.Get_infos_envs import Get_infos_envs
from utils.communication.get.Get_current_mode import Get_current_mode

class Client_statique:
    client = Client()

    @classmethod
    def get_client(self):
        return self.client

    @classmethod
    def get_infos_envi(self):
        return self.client.send(Get_infos_envs())

    @classmethod
    def get_current_mode(self):
        return self.client.send(Get_current_mode())
