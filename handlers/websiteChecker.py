import requests
import hashlib

url = "https://www.imperial.ac.uk/students/accommodation/current-residents/vacancies/"
headers = {'User-Agent': 'Mozilla/5.0'}


def get_site() -> str:
    response = requests.get(url, headers=headers)
    return str(response.content)


def convert_to_hash(string: str) -> str:
    return hashlib.sha224(string).hexdigest()


def check_new_hash(string: str) -> bool:
    if string not in hashes:
        hashes.append(string)
        return True
    else:
        return False


hashes = []
