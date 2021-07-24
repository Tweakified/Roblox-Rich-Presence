from setup import setup
from pypresence import Client
import time
import requests
import json
import os

def main():
    def isDiscordRunning():
        counter = 0
        r = os.popen('tasklist /v').read().strip().split('\n')
        for i in range(len(r)):
            s = r[i]
            if "Discord.exe" in r[i]:
                counter = counter + 1
        if counter >= 4:
            return True
        else:
            return False

    client_id = "696685746832277534"

    previous = {
        "details": None,
        "state": None,
        "image": None,
        "gameSize": None,
        "gameId": None,
    }
    start = None
    activityCleared = True

    client = None
    ClientClosed = True

    try:
        with open(os.path.abspath(os.getcwd()) + '\data.json') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = setup()

    discordToken = data["discordToken"]
    robloxId = data["robloxId"]

    while True:
        while isDiscordRunning() == True:
            if ClientClosed == True:
                client = Client(client_id)
                client.start()
                client.authenticate(discordToken)
                ClientClosed = False

            headers = {
                "previous": json.dumps(previous),
                "robloxId": str(robloxId),
            }
            rawData = requests.get("https://rich-presence-api.glitch.me/getStatus", headers=headers)
            if rawData.status_code == 200:
                data = rawData.json()
                details = data["details"]
                state = data["state"]
                image = data["image"]
                gameSize = data["gameSize"]
                gameId = data["gameId"]
                
                if details == None:
                    if activityCleared == False:
                        client.clear_activity()
                        activityCleared = True
                    else:
                        time.sleep(5)
                else:
                    if data != previous:
                        if details != previous["details"] or state != previous["state"] or gameId != previous["gameId"]:
                            start = round(time.time())
                        if details == "Playing":
                            client.set_activity(state=state, details=details, start=start, large_image=image, party_size=gameSize, large_text="Made by Tweakified")
                        else:
                            client.set_activity(state=state, details=details, start=start, large_image=image, large_text="Made by Tweakified")
                        activityCleared = False
                        time.sleep(15)
                    else:
                        time.sleep(5)
                previous = data
                    
        if ClientClosed == False:
            if client != None:
                client.close()
                ClientClosed = True

if __name__ == "__main__":
    main()
