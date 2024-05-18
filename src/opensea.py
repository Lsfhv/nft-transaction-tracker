from src.marketplace import Marketplace 
from src.trade import Trade
from src.eth_node import EthNode
from hexbytes import HexBytes
from pymongo import MongoClient
import asyncio
import json
from src.constants import (
    WETH_CONTRACT_ADDRESS, 
    MarketType,
    SIDE,
    OPENSEA_ORDER_FULFILLED_TOPIC
)

class Opensea(Marketplace):
    
    def __init__(self, aq: asyncio.Queue, eth_node: EthNode, client: MongoClient):
        super().__init__(aq, eth_node, client)
        with open('src/abi/openseaABI.json') as f:
            abi = json.load(f)
        self.contract = self.ethNode.w3.eth.contract(abi = abi)

        self.getEvent = {
            OPENSEA_ORDER_FULFILLED_TOPIC: self.contract.events.OrderFulfilled()
        }
        
    def getPrice(self, decoded) -> int:
        offer = decoded['args']['offer']
        consideration = decoded['args']['consideration']

        offerer = decoded['args']['offerer']    
        recipient = decoded['args']['recipient']

        x = {offerer, recipient}

        offer = [i for i in offer if i['itemType'] == 0 or (i['itemType'] == 1 and HexBytes(i['token']) == WETH_CONTRACT_ADDRESS)]
        consideration = [i for i in consideration if i['itemType'] == 0 or (i['itemType'] == 1 and HexBytes(i['token']) == WETH_CONTRACT_ADDRESS)]

        price = 0
        fee = 0

        if len(offer) != 0:
            for i in offer:
                price += i['amount']
        
            if len(consideration) != 0:
                for i in consideration:
                    if i['recipient'] not in x:
                        fee += i['amount']
        else:
            for i in consideration:
                price += i['amount']
                if i['recipient'] not in x:
                    fee += i['amount']
                

        feePercent = fee / price 
        return {
            'price': price, 
            'fee': int(feePercent * 10 ** 4),
        }
    
    # get collection address, token id and the side    
    def helper(self, decoded: dict) -> dict:
        offer = [i for i in decoded['args']['offer'] if i['itemType'] == 2] 
        consideration = [i for i in decoded['args']['consideration'] if i['itemType'] == 2]

        result = {}
        tradeType = SIDE.BUY
        if len(offer) == 0:
            offer, consideration = consideration, offer
            tradeType = SIDE.SELL
        
        return {
            'collectionAddress': HexBytes(offer[0]['token']), 
            'tokenId': HexBytes(offer[0]['identifier']),
            'side': tradeType
        }

    def decode(self, message: dict) -> Trade: 
        message = self.transform_msg(message)
        topic = message['topics'][0].hex()
        event = self.getEvent[topic]
        decoded = event.process_log(message)
       
        txHash = decoded['transactionHash']

        offerer = decoded['args']['offerer']
        recipient = decoded['args']['recipient']

        x = self.helper(decoded)

        if x['side'] == SIDE.SELL:
            offerer, recipient = recipient, offerer

        z = self.getPrice(decoded)
        price = z['price']
        fee = z['fee'] / 10 ** 4

        trade =  Trade(
            txHash, 
            HexBytes(offerer), 
            HexBytes(recipient),
            x['tokenId'], 
            x['collectionAddress'],  
            HexBytes(price),
            fee,
            HexBytes(0), 
            x['side'], 
            self.ethNode.getTimestamp(txHash),
            MarketType.OPENSEA
        )

        return trade
        