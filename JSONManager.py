from json import dump, load
from APIManager import getBazaarData

def write(fileName: str = "bazaar.json", dictionary: dict = None) -> None:
    if dictionary == None:
        dictionary = getBazaarData()
    with open(fileName, "w") as file:
        dump(dictionary, file, indent = 4)

def read(fileName: str = "bazaar.json") -> dict:
    with open(fileName, "r") as file:
        dictionary: dict = load(file)
        return dictionary