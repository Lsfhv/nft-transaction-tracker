import asyncio
from src.trade import Trade, TradeType, MarketType
from src.eth_node import EthNode
from hexbytes import HexBytes
from pymongo import MongoClient

from src.marketplace import Marketplace

class Blur(Marketplace): 
    def __init__(self, aq: asyncio.Queue, ethNode: EthNode, client: MongoClient): 
        super().__init__(aq, ethNode, client)
    
    def decode(self,message: dict) -> Trade:

        def splitData(data: HexBytes) -> list[HexBytes]:
            data = data.hex()
            data = data[2:]
            tokenIdListingIndexTrader = data[64:128]
            collectionPriceSide = data[128:192]
            takeFeeRecipientRate = data[192:]

            trader = HexBytes(tokenIdListingIndexTrader[len(tokenIdListingIndexTrader) - 40:]) # without 0x
            tokenId = HexBytes(tokenIdListingIndexTrader[:len(tokenIdListingIndexTrader) - 42]) 

            colAdd = HexBytes(collectionPriceSide[len(collectionPriceSide) - 40:]) # without 0x
            price = HexBytes(collectionPriceSide[2:len(collectionPriceSide) - 40])
            side = HexBytes(collectionPriceSide[:2])

            feeAdd = HexBytes(takeFeeRecipientRate[len(takeFeeRecipientRate) - 40:]) # without 0x
            fee = HexBytes(takeFeeRecipientRate[:len(takeFeeRecipientRate) - 40]) # x * 10 ** -4

            return [trader, 
                    tokenId,
                    colAdd,
                    price,
                    feeAdd,
                    fee, 
                    side]
        
        txHash = message['transactionHash']
        # print(f"txHash: {txHash.hex()}")
        txTopics = self.txTopics(txHash)

        trader, tokenId, colAdd, price, feeAdd, fee, side = splitData(message['data'])    

        dest = self.findDest(txTopics, trader, tokenId, side)

        if side == HexBytes(1):
            trader,dest = dest,trader

        return Trade(
            txHash, 
            trader, 
            dest,
            tokenId, 
            colAdd, 
            price,
            fee, 
            feeAdd, 
            TradeType.MAKER if side == HexBytes(0) else TradeType.TAKER, 
            self.ethNode.getTimestamp(txHash), 
            MarketType.BLUR
        )


