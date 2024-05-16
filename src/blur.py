import asyncio
from src.trade import Trade, TradeType
from src.constants import MarketType, Side
from src.eth_node import EthNode
from hexbytes import HexBytes
from pymongo import MongoClient
from src.marketplace import Marketplace


class Blur(Marketplace):
    def __init__(self, aq: asyncio.Queue, eth_node: EthNode, client: MongoClient):
        super().__init__(aq, eth_node, client)

    def decode(self, message: dict) -> Trade:
        def splitData(data: HexBytes) -> list[HexBytes]:

            data = data[2:]
            tokenIdListingIndexTrader = data[64:128]
            collectionPriceSide = data[128:192]
            takeFeeRecipientRate = data[192:]

            trader = HexBytes(tokenIdListingIndexTrader[len(tokenIdListingIndexTrader) - 40:])  # without 0x
            tokenId = HexBytes(tokenIdListingIndexTrader[:len(tokenIdListingIndexTrader) - 42])

            colAdd = HexBytes(collectionPriceSide[len(collectionPriceSide) - 40:])  # without 0x
            price = HexBytes(collectionPriceSide[2:len(collectionPriceSide) - 40])
            side = HexBytes(collectionPriceSide[:2])

            feeAdd = HexBytes(takeFeeRecipientRate[len(takeFeeRecipientRate) - 40:])  # without 0x
            fee = int(HexBytes(takeFeeRecipientRate[:len(takeFeeRecipientRate) - 40]).hex(),16)*(10**-4)  # x * 10 ** -4

            return [trader,
                    tokenId,
                    colAdd,
                    price,
                    feeAdd,
                    fee,
                    Side.MAKER if side == HexBytes(0) else Side.TAKER]

        txHash = message['transactionHash']
        trader, tokenId, colAdd, price, feeAdd, fee, side = splitData(message['data'])
        src_dest = self.get_src_dst(txHash, trader, tokenId, side)
        return Trade(
            txHash,
            src_dest['src'],
            src_dest['dst'],
            tokenId,
            colAdd,
            price,
            fee,
            feeAdd,
            side,
            self.ethNode.getTimestamp(txHash),
            MarketType.BLUR
        )
