from pypresence import Client
import requests
import json
import os

client_id = "696685746832277534"

def setup():
    client = Client(client_id)
    client.start()
    auth = client.authorize(client_id, ['rpc'])
    client.close()
    rpcToken = auth["data"]["code"]

    if rpcToken != None:
        headers = {
            "rpcToken": rpcToken,
        }
        user_object = requests.get("https://rich-presence-api.glitch.me/setup", headers=headers)
        if user_object.status_code == 200:
            user_json = user_object.json()
                
            with open(os.path.abspath(os.getcwd()) + '\data.json','w') as outfile:
                json.dump(user_json, outfile)
                    
            return user_json
        else:
            raise RuntimeWarning("One or more of the apis errored.")
    else:
        raise RuntimeWarning("Error when obtaining RPC token.")

if __name__ == "__main__":
    setup()
