from web3 import Web3
from datetime import datetime
from hexbytes import HexBytes


class EthNode:
    def __init__(self, key: str): 
        self.w3 = Web3(Web3.HTTPProvider(f"https://mainnet.infura.io/v3/{key}"))    

    def getTimestamp(self, txHash: str | HexBytes) -> datetime:
        block = self.w3.eth.get_transaction(txHash)['blockNumber']
        unixTime =  self.w3.eth.get_block(block)['timestamp']
        return datetime.utcfromtimestamp(unixTime)

    def getLogs(self, txHash: str | HexBytes) -> list:
        return self.w3.eth.get_transaction_receipt(txHash)['logs']
    
    