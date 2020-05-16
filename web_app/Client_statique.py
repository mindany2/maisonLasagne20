from utils.Client import Client

class Client_statique:
    client = Client()

    @classmethod
    def get_client(self):
        return self.client

