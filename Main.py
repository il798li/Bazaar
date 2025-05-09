from __future__ import annotations
from typing import Union
from datetime import datetime
from enum import Enum
from APIManager import getBazaarData
from time import sleep

class TradeType(Enum):
    sell = "sell"
    buy = "buy"

class TradeSummary:
    def __init__(self: TradeSummary, price: float, amount: int, tradeType: TradeType = TradeType.buy):
        self.price: float = price
        self.amount: float = amount
        self.tradeType: TradeType = tradeType

    def fromDictionary(dictionary: dict, tradeType: TradeType = TradeType.buy) -> TradeSummary:
        return TradeSummary(dictionary["pricePerUnit"], dictionary["amount"], tradeType)

class BazaarItem:
    def __init__(self: BazaarItem, productID: str, data: dict = None):
        self.productID: str = productID
        if data == None:
            data = getBazaarData()
        bazaarItemData: dict = data["products"][self.productID]
        self.buySummary: list[TradeSummary] = []
        self.sellSummary: list[TradeSummary] = []
        for buySummary in bazaarItemData["buy_summary"]:
            tradeSummary: TradeSummary = TradeSummary.fromDictionary(buySummary)
            self.buySummary.append(tradeSummary)
        for sellSummary in bazaarItemData["sell_summary"]:
            tradeSummary: TradeSummary = TradeSummary.fromDictionary(sellSummary, TradeType.sell)
            self.sellSummary.append(tradeSummary)
    
    def getInstantSellVolume(self: BazaarItem) -> int:
        instantSellVolume: int = 0
        for sellSummary in self.sellSummary:
            instantSellVolume += sellSummary.amount
        return instantSellVolume

class Item(BazaarItem):
    def __init__(self: Item, productID: str, data: dict, npcSell: float, display: str):
        super().__init__(productID, data)
        self.npcSell: float = npcSell
        self.display: str = display
    
    def estimateProfit(self: Item, relative: bool = False) -> float:
        buyOrderPrice: float = self.sellSummary[0].price + 0.1
        absoluteProfit: float = self.npcSell - buyOrderPrice
        if relative:
            absoluteProfit /= buyOrderPrice
        return absoluteProfit
    
    def calculateTotalInstantSellItems(self: Item) -> int:
        totalInstantSellItems: int = 0
        for buyOrder in self.sellSummary:
            totalInstantSellItems += buyOrder.amount
        return totalInstantSellItems
    
    def calculateScore(self: Item, oldItem: Union[Item, Snapshot]) -> float:
        if type(oldItem) == Snapshot:
            for item in oldItem.items:
                if item.productID == self.productID:
                    return self.calculateScore(item)
        oldBuyOrders: int = oldItem.calculateTotalInstantSellItems()
        newBuyOrders: int = self.calculateTotalInstantSellItems()
        amountBought: int = oldBuyOrders - newBuyOrders
        score: float = amountBought * self.estimateProfit()
        return score
    
    def __str__(self: Item) -> str:
        return self.display

class Snapshot:
    def __init__(self: Snapshot):
        self.timestamp: float = datetime.now().timestamp()
        data: dict = getBazaarData()
        self.items: list[Item] = [
            Item("ENCHANTED_HAY_BALE", data, 153_600, "Enchanted Hay Bale"),
            Item("MUTANT_NETHER_STALK", data, 102_400, "Mutant Nether Wart"),
            Item("BOX_OF_SEEDS", data, 76_800, "Box of Seeds"),
            Item("ENCHANTED_BAKED_POTATO", data, 76_800, "Enchanted Baked Potato"),
            Item("POLISHED_PUMPKIN", data, 256_000, "Polished Pumpkin"),
            Item("ENCHANTED_MELON_BLOCK", data, 51_200, "Enchanted Melon Block"),
            Item("ENCHANTED_HUGE_MUSHROOM_1", data, 51_200, "Enchanted Brown Mushroom Block"),
            Item("ENCHANTED_HUGE_MUSHROOM_2", data, 51_200, "Enchanted Red Mushroom Block"),
            Item("ENCHANTED_CACTUS", data, 102_400, "Enchanted Cactus"),
            Item("ENCHANTED_GRILLED_PORK", data, 128_000, "Enchanted Grilled Pork"),
            Item("ENCHANTED_COOKED_MUTTON", data, 128_000, "Enchanted Cooked Mutton")
        ]
    
    def findBestScore(self: Snapshot, oldSnapshot: Snapshot) -> Item:
        bestScore: float = 0
        bestItem: Item = None
        for item in self.items:
            score: float = item.calculateScore(oldSnapshot)
            if score > bestScore:
                bestItem = item
                bestScore = score
        return bestItem

class Comparison:
    def __init__(self: Comparison):
        self.snapshots: list[Snapshot] = [Snapshot(), Snapshot()]
    
    def compare(self: Comparison) -> None:
        bestItem: Item = self.snapshots[1].findBestScore(self.snapshots[0])
        if bestItem != None:
            score: float = bestItem.calculateScore(self.snapshots[0])
            print(f"Item: {bestItem} | Score: {score}")
        self.nextSnapshot()
    
    def nextSnapshot(self: Comparison) -> None:
        self.snapshots[0] = self.snapshots[1]
        self.snapshots[1] = Snapshot()

comparison: Comparison = Comparison()

while True:
    try:
        comparison.compare()
    except Exception:
        pass