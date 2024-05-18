from enum import Enum
from hexbytes import HexBytes   
from datetime import datetime
from bson.decimal128 import Decimal128
from src.constants import MarketType, SIDE
import json
import ast

class Trade:
    def __init__(
        self,
        txHash: str, 
        source: HexBytes, 
        destination: HexBytes, 
        tokenId: HexBytes,
        collectionAddress: HexBytes, 
        price: HexBytes, 
        feeRate, 
        feeAddress: HexBytes, 
        side: SIDE, 
        timestamp: datetime, 
        market: MarketType):

        if not isinstance(txHash, str):
            raise TypeError("txHash must be a string")
        
        if not (isinstance(feeRate, float) or isinstance(feeRate, int)):
            raise TypeError("feeRate must be a float or int")
        
        if not (feeRate >= 0 and feeRate <= 1):
            raise ValueError("feeRate must be between 0 and 1")
        
        

        self.txHash = txHash
        self.source = source
        self.destination = destination
        self.tokenId = tokenId
        self.collectionAddress = collectionAddress
        self.price = price
        self.feeRate = feeRate
        self.feeAddress = feeAddress
        self.side = side
        self.timestamp = timestamp
        self.market = market


    # Returns a dictionary representation of the trade for db
    def get_trade_for_db(self) -> dict:
        result = json.loads(self.__str__())
        result['token_id'] = Decimal128(str(int(self.tokenId.hex(), 16)))
        result['price'] = Decimal128(str(int(self.price.hex(), 16)))
        return result
        
    
    def __eq__(self, other):
        return self.txHash == other.txHash and \
               self.source == other.source and \
               self.destination == other.destination and \
               int(self.tokenId.hex(),16) == int(other.tokenId.hex(),16) and \
               self.collectionAddress == other.collectionAddress and \
               int(self.price.hex(),16) == int(other.price.hex(),16) and \
               self.feeRate == other.feeRate and \
               self.feeAddress == other.feeAddress and \
               self.side == other.side and \
               self.timestamp == other.timestamp and \
               self.market == other.market
    
    def __str__(self):
        return json.dumps({
            'tx_hash': self.txHash, 
            'source': self.source.hex(),
            'destination': self.destination.hex(),
            'token_id': self.tokenId.hex(),
            'collection_address': self.collectionAddress.hex(),
            'price': self.price.hex(),
            'fee_rate': self.feeRate,
            'fee_address': self.feeAddress.hex(),
            'trade_type': self.side.name,
            'timestamp': self.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
            'market': self.market.name
        })
    