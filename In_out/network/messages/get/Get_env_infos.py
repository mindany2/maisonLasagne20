from In_out.network.messages.Message import Message

class Get_env_infos(Message):

    def __init__(self, name):
        self.name = name

    def do(self, getter):
        return str(getter.get_tree().get_env(self.name))
