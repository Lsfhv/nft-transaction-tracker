import unittest
from src.marketplace import Marketplace
from hexbytes import HexBytes
import mongomock
import asyncio
from os import environ
from src.eth_node import EthNode
from src.blur import Blur
import pymongo
import logging
from test_data import BLUR_MAKER_MSG, SLEEP, TX_HASH, ADD_LEN
from src.constants import Side


class TestMarketplace(unittest.TestCase):
    def setUp(self):
        class TempMarketplace(Marketplace):
            def decode(self, message: dict):
                pass

        logging.getLogger().setLevel(logging.CRITICAL)  
        infura_key = environ["INFURAAPIKEY"]
        self.ethNode = EthNode(infura_key)
        self.mockClient = mongomock.MongoClient().nft
        self.marketplace = TempMarketplace(asyncio.Queue(), self.ethNode, self.mockClient)
        self.badMockClient = pymongo.MongoClient(host='192', serverSelectionTimeoutMS=1000).nft

        self.src_dst_input_1 = {
            'trader': HexBytes('0xd0bc13738D982F06399844480990a5Cf59B51867'), 
            'token_id': HexBytes(4097), 
            'side': Side.TAKER
        }

    def test_find_destination(self):
        src_dst = self.marketplace.get_src_dst(TX_HASH, self.src_dst_input_1['trader'], self.src_dst_input_1['token_id'], self.src_dst_input_1['side'])
        
        self.assertEqual(src_dst['src'], HexBytes('0x4Bb00e207989cFaCA6b9A767DE146FAc2a1104B4'))
        self.assertEqual(src_dst['dst'], HexBytes('0xd0bc13738D982F06399844480990a5Cf59B51867'))    

        self.assertEqual(len(src_dst['src'].hex()), ADD_LEN, f'Source address should be {ADD_LEN} characters long')
        self.assertEqual(len(src_dst['dst'].hex()), ADD_LEN, f'Destination address should be {ADD_LEN} characters long')

        # with multiple tx logs



    def test_tx_topics(self):
        tx_logs = self.marketplace.tx_logs(TX_HASH)
        self.assertEqual(len(tx_logs), 1)

    def test_buffer(self):
        blur = Blur(asyncio.Queue(), self.ethNode, self.badMockClient)

        async def test():
            asyncio.create_task(blur.start())
            await blur.aq.put(BLUR_MAKER_MSG)
            await asyncio.sleep(SLEEP)
            self.assertEqual(blur.buffer.qsize(), 1)

            await blur.aq.put(BLUR_MAKER_MSG)
            await asyncio.sleep(SLEEP)
            self.assertEqual(blur.buffer.qsize(), 2)

            await blur.aq.put(BLUR_MAKER_MSG)
            await asyncio.sleep(SLEEP)
            self.assertEqual(blur.buffer.qsize(), 3)

            # switch to good client, should clear the buffer after getting a new msg
            blur.client = self.mockClient

            await blur.aq.put(BLUR_MAKER_MSG)
            await asyncio.sleep(SLEEP)
            self.assertEqual(blur.buffer.qsize(), 0)

            # 4 items in the database
            trades = blur.client.trades.find()
            self.assertEqual(len(list(trades)), 4)

        asyncio.run(test())
