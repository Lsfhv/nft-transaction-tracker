from src.marketplace import Marketplace
from src.trade import Trade
import asyncio 
from src.eth_node import EthNode 
from pymongo import MongoClient
import json
from hexbytes import HexBytes
from src.constants import (
    Side, 
    MAGICEDEN_ACCEPT_OFFER_ERC721_TOPIC, 
    MAGICEDEN_BUY_LISTING_ERC721_TOPIC,
    MarketType
)

class MagicEden(Marketplace):

    def __init__(self, aq: asyncio.Queue, eth_node: EthNode, client: MongoClient):
        super().__init__(aq, eth_node, client)

        with open('src/abi/magicedenABI.json') as f:
            abi = json.load(f)
        
        self.contract = self.ethNode.w3.eth.contract(abi = abi)

        self.getEvent = {
            MAGICEDEN_ACCEPT_OFFER_ERC721_TOPIC: self.contract.events.AcceptOfferERC721(), 
            MAGICEDEN_BUY_LISTING_ERC721_TOPIC: self.contract.events.BuyListingERC721()
        }

    def get_side(self, topic: str) -> Side:
        return Side.SELL if topic == MAGICEDEN_ACCEPT_OFFER_ERC721_TOPIC else Side.BUY

    def decode(self, message: dict) -> Trade:
        message = self.transform_msg(message)
        topic = message['topics'][0].hex()
        event = self.getEvent[topic]
        decoded = event.process_log(message)
        
        return Trade(
            decoded['transactionHash'],
            HexBytes(decoded['args']['seller']),
            HexBytes(decoded['args']['buyer']),
            HexBytes(decoded['args']['tokenId']),
            HexBytes(decoded['args']['tokenAddress']),
            HexBytes(decoded['args']['salePrice']),
            0, 
            HexBytes(0),
            self.get_side(topic), 
            self.ethNode.getTimestamp(decoded['transactionHash']),
            MarketType.MAGICEDEN
        ) 
