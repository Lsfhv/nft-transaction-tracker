from src.marketplace import Marketplace
from src.trade import Trade, TradeType, MarketType
import asyncio 
from src.eth_node import EthNode 
from pymongo import MongoClient
import json
from hexbytes import HexBytes

class MagicEden(Marketplace):

    def __init__(self, aq: asyncio.Queue, eth_node: EthNode, client: MongoClient):
        super().__init__(aq, eth_node, client)

        with open('src/abi/magicedenABI.json') as f:
            abi = json.load(f)
        self.contract = self.ethNode.w3.eth.contract(abi = abi)

        self.getEvent = {
            HexBytes('0x8b87c0b049fe52718fe6ff466b514c5a93c405fb0de8fbd761a23483f9f9e198'): self.contract.events.AcceptOfferERC721(), 
            HexBytes('0xffb29e9cf48456d56b6d414855b66a7ec060ce2054dcb124a1876310e1b7355c'): self.contract.events.BuyListingERC721()
        }

    def side(self, topic: str) -> TradeType:
        if topic == '0x8b87c0b049fe52718fe6ff466b514c5a93c405fb0de8fbd761a23483f9f9e198':
            return TradeType.TAKER
        else:
            return TradeType.MAKER

    def decode(self, message: dict) -> Trade:
        topic = message['topics'][0]    
        event = self.getEvent[topic]
        decoded = event.process_log(message)
    
        return Trade(
            decoded['transactionHash'],
            HexBytes(decoded['args']['seller']),
            HexBytes(decoded['args']['buyer']),
            HexBytes(decoded['args']['tokenId']),
            HexBytes(decoded['args']['tokenAddress']),
            HexBytes(decoded['args']['salePrice']),
            HexBytes(0), 
            HexBytes(0),
            self.side(topic), 
            self.ethNode.getTimestamp(decoded['transactionHash']),
            MarketType.MAGICEDEN
        ) 

# 0xffb29e9cf48456d56b6d414855b66a7ec060ce2054dcb124a1876310e1b7355c