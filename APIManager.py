import requests
from os import getenv

def getBazaarData() -> dict:
    apiKey: str = getenv("API_KEY")
    if apiKey == None:
        raise Exception("You have not provided an API key!")
    url: str = f"https://api.hypixel.net/skyblock/bazaar?key={apiKey}"
    response: requests.Response = requests.get(url)
    return response.json()