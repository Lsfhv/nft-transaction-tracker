from src.marketplace import Marketplace 
from src.trade import Trade, TradeType, MarketType
from src.eth_node import EthNode
from hexbytes import HexBytes
from pymongo import MongoClient
import asyncio

class Opensea(Marketplace):

    def __init__(self, aq: asyncio.Queue, ethNode: EthNode, client: MongoClient):
        super().__init__(aq, ethNode, client)   
    
    def decodeOSlog(self, log: dict) -> dict:
        return self.ethNode.decodeOSlog(log)

    def decode(self, message: dict) -> Trade: 
        log = self.decodeOSlog(message)
        
        print("got opensea trade")