#!/usr/bin/env python3
import sys
from In_out.network.Client import Client
from In_out.network.messages.get.Get_env_infos import Get_env_infos
from In_out.network.messages.get.Get_tree_infos import Get_tree_infos

def main():
    if len(sys.argv) < 2:
        message = Get_tree_infos()
    else:
        message = Get_env_infos(sys.argv[1])
    client = Client()
    client.start()
    print(client.send(message))
    client.disconnect()

if __name__ == "__main__":
    main()

