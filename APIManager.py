import requests

def getBazaarData() -> dict:
    url: str = f"https://api.hypixel.net/skyblock/bazaar"
    response: requests.Response = requests.get(url)
    return response.json()