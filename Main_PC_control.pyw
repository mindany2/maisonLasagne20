
"""
Programme python éxécuter par le PC 
pour recevoir les ordres du rpi
"""

from In_out.network.Server import Server

Server(None).start()

while(1):
	pass