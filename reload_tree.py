#!/usr/bin/env python3
from In_out.network.Client import Client
from In_out.network.messages.Reload_tree import Reload_tree
from time import sleep

client = Client()
client.start()
data = client.send(Reload_tree())
if data:
    print(data)
client.disconnect()
