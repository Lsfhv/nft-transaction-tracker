import asyncio
from trade import Trade, TradeType, MarketType
from eth_node import EthNode
from hexbytes import HexBytes
from pymongo import MongoClient
class Blur: 
    def __init__(self, aq: asyncio.Queue, ethNode: EthNode): 
        self.aq = aq 
        self.ethNode = ethNode
        self.txTopic = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'
        self.rhb = lambda x : HexBytes(int(x.hex(), 16))

        self.client = MongoClient('192.168.0.6', 27017).nft 
    
    def txTopics(self, txHash: str) -> list:
        logs = self.ethNode.getLogs(txHash)
        return [i['topics'] for i in logs if i['topics'][0].hex() == self.txTopic and len(i['topics']) == 4]
    
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
        
        def hbEq(hb1: HexBytes, hb2: HexBytes) -> bool:
            return self.rhb(hb1) == self.rhb(hb2)
        
        def findDest(txTopics: list, trader: HexBytes, tokenId: HexBytes, side: HexBytes) -> HexBytes:

            src, dest = 1,2 
            if side == HexBytes(1): 
                src, dest = dest, src

            txTopics = [
                i for i in txTopics if hbEq(i[3], tokenId) and hbEq(i[src], trader)]
            return self.rhb(txTopics[0][dest])
        
        txHash = message['transactionHash']
        print(txHash.hex())
        txTopics = self.txTopics(txHash)

        trader, tokenId, colAdd, price, feeAdd, fee, side = splitData(message['data'])    

        dest = findDest(txTopics, trader, tokenId, side)

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

    
    async def start(self) -> None:
        while True: 
            message = await self.aq.get()
            try:
                print('------------------------------------------------------------------------------')
                trade = self.decode(message)  
                self.client.trades.insert_one(trade.getDict())
                print('------------------------------------------------------------------------------')
            except:
                print('Error')

