#!/usr/bin/env python3
import os
from In_out.network.Client import Client
from In_out.network.messages.interrupt.Spotify_inter import Spotify_inter
from time import sleep

event = os.environ.get("PLAYER_EVENT")
volume = os.environ.get("VOLUME")
track = os.environ.get("TRACK_ID")
position = os.environ.get("POSITION_MS")

VOLUME_MAX = 65535

if volume:
    volume = float(volume)/VOLUME_MAX*100

client = Client()
client.start()
data = client.send(Spotify_inter(event, volume, track, position))
if data:
    print(data)
