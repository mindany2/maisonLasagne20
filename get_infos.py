#!/usr/bin/env python3
import sys
from In_out.network.Client import Client
from In_out.network.messages.get.Get_env_infos import Get_env_infos

def main():
    if len(sys.argv) < 2:
        print("Usage : env_name")
        return 
    name = sys.argv[1]
    client = Client()
    client.start()
    print(client.send(Get_env_infos(name)))

if __name__ == "__main__":
    main()

