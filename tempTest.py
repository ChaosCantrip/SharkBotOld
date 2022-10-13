import json
import os

files = [f"data/live/members/{filename}" for filename in os.listdir("data/live/members")]

for filename in files:
    try:
        with open(filename, "r") as infile:
            data = json.load(infile)
        print(f"{filename} fine")
    except Exception as e:
        print(f"{filename} fucked ({e})")