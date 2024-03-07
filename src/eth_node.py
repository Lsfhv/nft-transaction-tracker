from web3 import Web3, AsyncWeb3
from web3.providers import WebsocketProviderV2
import asyncio
from datetime import datetime
from hexbytes import HexBytes
class EthNode:
    def __init__(self, key: str): 
        self.w3 = Web3(Web3.HTTPProvider(f"https://mainnet.infura.io/v3/{key}"))    

        self.makerT = "0x7dc5c0699ac8dd5250cbe368a2fc3b4a2daadb120ad07f6cccea29f83482686e"
        self.takerT = "0x0fcf17fac114131b10f37b183c6a60f905911e52802caeeb3e6ea210398b81ab"

    # get timestamp of tx in unix time
    def getTimestamp(self, txHash: str | HexBytes) -> datetime:
        block = self.w3.eth.get_transaction(txHash)['blockNumber']
        unixTime =  self.w3.eth.get_block(block)['timestamp']
        return datetime.utcfromtimestamp(unixTime)

    # Returns the logs of a transaction
    def getLogs(self, txHash: str | HexBytes) -> list:
        return self.w3.eth.get_transaction_receipt(txHash)['logs']
    
    async def w2Logs(self, q: asyncio.Queue, key: str):
        async with AsyncWeb3.persistent_websocket(
            WebsocketProviderV2(f"wss://mainnet.infura.io/ws/v3/{key}")
        ) as w3:

            await w3.eth.subscribe("logs", {
                "address": "0xb2ecfE4E4D61f8790bbb9DE2D1259B9e2410CEA5",
                "topics": [self.makerT]
                }) 
            
            await w3.eth.subscribe("logs", {
                "address": "0xb2ecfE4E4D61f8790bbb9DE2D1259B9e2410CEA5",
                "topics": [self.takerT]
                }) 
            async for response in w3.ws.process_subscriptions():
                await q.put(response['result'])

    