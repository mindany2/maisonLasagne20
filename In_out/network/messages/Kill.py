from In_out.network.messages.Message import Message

class Kill(Message):
    """
    """

    def __init__(self):
        Message.__init__(self)

    def return_value(self):
        return False
