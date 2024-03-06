from enum import Enum
from hexbytes import HexBytes   
from datetime import datetime
from bson.decimal128 import Decimal128

class TradeType(Enum):
    # Someone bought a listed item
    MAKER = "MAKER" 

    # Someone sold into a bid
    TAKER = "TAKER" 

class MarketType(Enum):
    OPENSEA = "OPENSEA"
    BLUR = "BLUR"
    MAGICEDEN = "MAGICEDEN"

class Trade:
    def __init__(
        self,
        txHash: HexBytes, 
        source: HexBytes, 
        destination: HexBytes, 
        tokenId: HexBytes,
        collectionAddress: HexBytes, 
        price: HexBytes, 
        feeRate: HexBytes, 
        feeAddress: HexBytes, 
        tradeType: TradeType, 
        timestamp: datetime, 
        market: MarketType):

        self.txHash = txHash
        self.source = source
        self.destination = destination
        self.tokenId = tokenId
        self.collectionAddress = collectionAddress
        self.price = price
        self.feeRate = feeRate
        self.feeAddress = feeAddress
        self.tradeType = tradeType
        self.timestamp = timestamp
        self.market = market

    # Returns a dictionary representation of the trade for db
    def getDict(self) -> dict:
        return {
            "txHash" : self.txHash.hex(), 
            "source" : self.source.hex(),
            "destination" : self.destination.hex(),
            "tokenId" : int(self.tokenId.hex(), 16),
            "collectionAddress" : self.collectionAddress.hex(),
            "price" : Decimal128(str(int(self.price.hex(), 16))),
            "feeRate" : int(self.feeRate.hex(), 16),
            "feeAddress" : self.feeAddress.hex(),
            "tradeType" : self.tradeType.value,
            "timestamp" : self.timestamp.strftime("%Y-%m-%d %H:%M:%S"), 
            "market" : self.market.value
        }
    
    def getStringDict(self) -> dict:
        return {
            "txHash": self.txHash.hex(),
            "source": self.source.hex(),
            "destination": self.destination.hex(),
            "tokenId": self.tokenId.hex(),
            "collectionAddress": self.collectionAddress.hex(),
            "price": self.price.hex(),
            "feeRate": self.feeRate.hex(),
            "feeAddress": self.feeAddress.hex(),
            "tradeType": self.tradeType.name, 
            "timestamp": self.timestamp
        }
    
    def __str__(self):
        return str(self.getStringDict())
    