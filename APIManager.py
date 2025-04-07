import requests
from os import getenv

apiKey: str = getenv("API_KEY")
url: str = f"https://api.hypixel.net/skyblock/bazaar?key={apiKey}"

def getBazaarData() -> dict:
    response: requests.Response = requests.get(url)
    return response.json()