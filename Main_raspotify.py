#!/usr/bin/env python3
import os
from utils.Client import Client

event = os.environ.get("PLAYER_EVENT")

if (event == "playing") or (event == "paused") or (event == "stop"):
    client = Client()
    client.send("spotify_inter(\"{}\")".format(event))
