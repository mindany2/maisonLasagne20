#!/usr/bin/env python3
from utils.communication.Client import Client
from utils.communication.Repair import Repair
from threading import Thread

client = Client()
Thread(target = client.send, args=[Repair()]).start()
