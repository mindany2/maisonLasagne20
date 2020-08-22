#!/usr/bin/env python3
from utils.communication.Client import Client
from utils.communication.Reload_tree import Reload_tree

client = Client()
client.send(Reload_tree())
