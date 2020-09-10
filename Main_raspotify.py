#!/usr/bin/env python3
import os
from utils.communication.Client import Client
from utils.communication.Spotify_inter import Spotify_inter

event = os.environ.get("PLAYER_EVENT")
volume = os.environ.get("VOLUME")

VOLUME_MAX = 65535

if volume:
    volume = float(volume)/VOLUME_MAX*100

client = Client()
client.send(Spotify_inter(event, volume))
