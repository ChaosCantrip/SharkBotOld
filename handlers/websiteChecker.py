import requests
import hashlib
import time
import json
import os

hashFilepath = "data/websiteHashes.json"

url = "https://www.imperial.ac.uk/students/accommodation/current-residents/vacancies/"
headers = {'User-Agent': 'Mozilla/5.0'}


def get_site() -> bytes:
    response = requests.get(url, headers=headers)
    return response.content


def convert_to_hash(string: bytes) -> str:
    return hashlib.sha224(string).hexdigest()


def check_new_hash(string: str) -> bool:
    if string not in hashes:
        hashes.append(string)
        with open(hashFilepath, "w") as outfile:
            json.dump(outfile, hashes)
        return True
    else:
        return False


if not os.path.exists(hashFilepath):  # Make sure hashes file exists
    open(hashFilepath, "w").close()

with open(hashFilepath, "r") as infile:
    hashes = json.load(infile)

if __name__ == "__main__":
    while True:
        siteString = get_site()
        siteHash = convert_to_hash(siteString)
        if check_new_hash(siteHash):
            print(f"New Hash: {siteHash}")
        else:
            print(f"Old Hash: {siteHash}")
        time.sleep(5)

