from abc import ABC, abstractmethod
from src.trade import Trade
import asyncio
from src.eth_node import EthNode
from pymongo import MongoClient
from hexbytes import HexBytes
import queue
import logging
from src.constants import SIDE
from web3.datastructures import AttributeDict

logger = logging.getLogger(__name__)


class Marketplace(ABC):

    def __init__(self, aq: asyncio.Queue, eth_node: EthNode, client: MongoClient):
        self.aq = aq
        self.ethNode = eth_node
        self.txTopic = '0xddf252ad1be2c89b69c2b068fc378daa952ba7f163c4a11628f55a4df523b3ef'
        self.rhb = lambda x: HexBytes(int(x.hex(), 16))

        self.client = client
        self.buffer = queue.Queue()
        self.messageBuffer = queue.Queue()

    def tx_logs(self, tx_hash: str) -> list:
        """Method to get the transaction topics from a transaction hash

        Args:
            tx_hash (str): transaction hash

        Returns:
            list: list of transaction topics
        """
        logs = self.ethNode.getLogs(tx_hash)
        return [i['topics'] for i in logs if i['topics'][0].hex() == self.txTopic and len(i['topics']) == 4]

    def hbEq(self, hb1: HexBytes, hb2: HexBytes) -> bool:
        return self.rhb(hb1) == self.rhb(hb2)

    @abstractmethod
    def decode(self, message: dict) -> Trade:
        """Method to decode the message

        Args:
            message (dict): message to decode

        Returns:
            Trade: Trade object
        """
        pass

    def pad_add_to_eth_add_len(self, address: HexBytes) -> HexBytes:
        """Method to pad address with 0 to 42 characters including 0x

        Args:
            address (HexBytes): address to pad

        Returns:
            HexBytes: padded address
        """

        suffix_len = len(address.hex())
        if 42 - suffix_len < 0:
            raise ValueError("Address is longer than 42 characters")

        return HexBytes('0x' + '0' * (42 - len(address.hex())) + address.hex()[2:])

    def get_src_dst(self, tx_hash: str, trader: HexBytes, tokenId: HexBytes, side: SIDE) -> dict:
        src, dest = 1, 2

        if side == SIDE.SELL:
            src, dest = dest, src

        tx_logs = self.tx_logs(tx_hash)

        tx_logs = [
            i for i in tx_logs if self.hbEq(i[3], tokenId) and self.hbEq(i[src], trader)]
        
        x = self.pad_add_to_eth_add_len(self.rhb(tx_logs[0][dest]))

        if side == SIDE.SELL:
            trader, x = x, trader   

        return {
            "src": trader,
            "dst": x
        }
    
    def transform_msg(self, message: dict) -> AttributeDict:
        """Transform msg so it works with the web3 decode function

        Args:
            message (dict): msg from infura node

        Returns:
            AttributeDict: transformed msg
        """
        message['topics'] = [HexBytes(i) for i in message['topics']]
        return AttributeDict(message)

    def db_insert(self, trade: Trade) -> None:
        self.client.trades.insert_one(trade.get_trade_for_db())

    def clear_buffer(self) -> None:
        # TODO : IF MID WAY DB INSERT FAILS, A TRADE OBJECT WILL BE LOST
        try:
            while not self.buffer.empty():
                trade = self.buffer.get()
                self.db_insert(trade)
        except Exception as e:
            pass

    async def start(self) -> None:
        logger.info(f"Started {self.__class__.__name__}")
        while True:
            message = await self.aq.get()
            
            logger.info(f"Got a message: {message}")

            try:
                trade = self.decode(message)
            except Exception as e:                
                logger.error(f"Error decoding message: {e}")
                logging.error(f"Message: {message}")
                continue

            logger.info(f"Decoded message: {trade}")

            try:
                self.db_insert(trade)

                self.clear_buffer()
            except Exception as e:
                self.buffer.put(trade)
                
                logger.warning(f"No DB, so stored in memory: {self.buffer.qsize()} instances so far")
