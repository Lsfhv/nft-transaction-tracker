from web3 import Web3, AsyncWeb3
from web3.providers import WebsocketProviderV2
import asyncio
from datetime import datetime
from hexbytes import HexBytes
import json 
import logging 
from src.constants import BLUR_CONTRACT_ADDRESS

logger = logging.getLogger(__name__)

MAGICEDEN = '0x9A1D00bEd7CD04BCDA516d721A596eb22Aac6834'
AcceptOfferERC721 = '0x8b87c0b049fe52718fe6ff466b514c5a93c405fb0de8fbd761a23483f9f9e198'

class EthNode:
    def __init__(self, key: str): 
        self.w3 = Web3(Web3.HTTPProvider(f"https://mainnet.infura.io/v3/{key}"))    

        self.makerT = "0x7dc5c0699ac8dd5250cbe368a2fc3b4a2daadb120ad07f6cccea29f83482686e"
        self.takerT = "0x0fcf17fac114131b10f37b183c6a60f905911e52802caeeb3e6ea210398b81ab"

        with open('src/abi.json') as f:
            abi = json.load(f)
        self.contract = self.w3.eth.contract(abi = abi)

    # get timestamp of tx in unix time
    def getTimestamp(self, txHash: str | HexBytes) -> datetime:
        block = self.w3.eth.get_transaction(txHash)['blockNumber']
        unixTime =  self.w3.eth.get_block(block)['timestamp']
        return datetime.utcfromtimestamp(unixTime)

    # Returns the logs of a transaction
    def getLogs(self, txHash: str | HexBytes) -> list:
        return self.w3.eth.get_transaction_receipt(txHash)['logs']
    
    # def decodeOSlog(self, log: dict) -> dict:
    #     data = self.contract.events.OrderFulfilled().process_log(log)['args']
    #     return {k: v for k,v in data.items()}
    
    async def w2Logs(self, marketplaces, key: str):
        try:
            async with AsyncWeb3.persistent_websocket(
                WebsocketProviderV2(f"wss://mainnet.infura.io/ws/v3/{key}")
            ) as w3:
            
                submap = {}

                makersub = await w3.eth.subscribe("logs", {
                    "address": BLUR_CONTRACT_ADDRESS,
                    "topics": [self.makerT]
                    }) 
                
                takersub = await w3.eth.subscribe("logs", {
                    "address": BLUR_CONTRACT_ADDRESS,
                    "topics": [self.takerT]
                    }) 
                
                # orderfulfilled = await w3.eth.subscribe("logs", {
                #     "address": '0x00000000000000ADc04C56Bf30aC9d3c0aAF14dC', 
                #     "topics": ['0x9d9af8e38d66c62e2c12f0225249fd9d721c54b83f48d9352c97c6cacdcb6f31']
                # })

                # magice eden 
                # magicEdenAcceptErc721 = await w3.eth.subscribe("logs", {
                #     "address": MAGICEDEN, 
                #     "topics": [AcceptOfferERC721]
                # })
                
                submap[makersub] = marketplaces[0] 
                submap[takersub] = marketplaces[0]

                # submap[magicEdenAcceptErc721] = marketplaces[2]

                # submap[orderfulfilled] = marketplaces[1]
                            
                async for response in w3.ws.process_subscriptions():
                    sub = response['subscription']
                    await submap[sub].aq.put(response['result'])
        except Exception as e:

            logger.critical(f"Websocket error: {e}")

    