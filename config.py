import json

ACCESS_TOKEN = "token"

with open("config.json") as config:
    data = json.load(config)

    ACCESS_TOKEN = data["token"]
