#!/usr/bin/env python3
import os
from utils.communication.Client import Client
from utils.communication.Spotify_inter import Spotify_inter

event = os.environ.get("PLAYER_EVENT")

if (event == "playing") or (event == "paused") or (event == "stop"):
    client = Client()
    client.send(Spotify_inter(event))
