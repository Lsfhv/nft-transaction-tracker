from abc import ABC, abstractmethod 
from src.trade import Trade 
import asyncio
from src.eth_node import EthNode
from pymongo import MongoClient
from hexbytes import HexBytes
import queue 

class Marketplace(ABC):

    def __init__(self, aq: asyncio.Queue, ethNode: EthNode, client: MongoClient):
        self.aq = aq 
        self.ethNode = ethNode
        self.txTopic = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'
        self.rhb = lambda x : HexBytes(int(x.hex(), 16))

        self.client = client
        self.buffer = queue.Queue() 
    
    def txTopics(self, txHash: str) -> list:
        logs = self.ethNode.getLogs(txHash)
        return [i['topics'] for i in logs if i['topics'][0].hex() == self.txTopic and len(i['topics']) == 4]
    
    def hbEq(self, hb1: HexBytes, hb2: HexBytes) -> bool:
        return self.rhb(hb1) == self.rhb(hb2)
    
    @abstractmethod 
    def decode(self, message: dict) -> Trade:
        pass

    # Pad the address to 42 characters
    def padAddress(self, address: HexBytes) -> HexBytes:
        return HexBytes('0x' + '0' * (42 - len(address.hex())) + address.hex()[2:])

    def findDest(self, txTopics: list, trader: HexBytes, tokenId: HexBytes, side: HexBytes) -> HexBytes:
        src, dest = 1,2 
        if side == HexBytes(1): 
            src, dest = dest, src

        txTopics = [
            i for i in txTopics if self.hbEq(i[3], tokenId) and self.hbEq(i[src], trader)]
        return self.padAddress(self.rhb(txTopics[0][dest]))

    async def start(self) -> None:
        while True: 
            message = await self.aq.get()
            try:
                trade = self.decode(message)
                try:
                    self.client.trades.insert_one(trade.getDict())
                    while not self.buffer.empty():
                        trade = self.buffer.queue[0]
                        self.client.trades.insert_one(trade) 
                        self.buffer.get()
                except:
                    self.buffer.put(trade.getDict())
                    print(f"Buffered, bring DB back before I run out of memory!! : {self.buffer.qsize()}")
            except Exception as e:
                print(e)  
