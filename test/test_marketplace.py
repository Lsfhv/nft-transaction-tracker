import unittest 
from src.marketplace import Marketplace
from hexbytes import HexBytes
import mongomock
import asyncio
from os import environ
from src.eth_node import EthNode
from src.blur import Blur 
import pymongo

class TestMarketplace(unittest.TestCase):
    def setUp(self):

        class TempMarketplace(Marketplace):
            def decode(self, message: dict):
                pass
        infuraKey = environ['INFURAAPIKEY']
        self.ethNode = EthNode(infuraKey)
        self.mockClient = mongomock.MongoClient().nft
        self.marketplace = TempMarketplace(asyncio.Queue(), self.ethNode, self.mockClient)
        self.badMockClient = pymongo.MongoClient(host='192',serverSelectionTimeoutMS=1000).nft 
        self.blurTx = '0x3976f2657aca7b7f99e2345418cb4a9abc6792a157cb09b9ad3206c846dec459'

        self.SLEEP = 0.1 # sleep to let the coroutine to switch to handle buffer

    def test_padAddress(self):
        self.assertEqual(self.marketplace.padAddress(HexBytes('0x1')), HexBytes('0x' + '0' * 39 + '1'))

    def test_insert_log(self):
        log = self.ethNode.getLogs(self.blurTx)[-1]
        blur = Blur(asyncio.Queue(), self.ethNode, self.mockClient)
        async def test():
            asyncio.create_task(blur.start())
            await blur.aq.put(log)
            await asyncio.sleep(self.SLEEP)

            trades = blur.client.trades.find()
            self.assertEqual(len(list(trades)), 1)
        asyncio.run(test())

    def test_messageBufferWithPermTradeIn(self):
        badtx = HexBytes('0x3976f2657aca7b7f99e2345418cb4a9abc6792a157cb09b9ad3206c846dec458')
        goodtx = HexBytes('0x3976f2657aca7b7f99e2345418cb4a9abc6792a157cb09b9ad3206c846dec459')
        blur = Blur(asyncio.Queue(), self.ethNode, self.mockClient)

        goodLog = dict(self.ethNode.getLogs(self.blurTx)[-1])
        goodLog['transactionHash'] = goodtx

        badLog = dict(self.ethNode.getLogs(self.blurTx)[-1])
        badLog['transactionHash'] = badtx

        async def test():
            asyncio.create_task(blur.start())
            await blur.aq.put(badLog)
            await asyncio.sleep(self.SLEEP)
            self.assertEqual(blur.messageBuffer.qsize(), 1)

            await blur.aq.put(goodLog)
            await asyncio.sleep(self.SLEEP)
            self.assertEqual(blur.messageBuffer.qsize(), 1)

            trades = blur.client.trades.find()
            self.assertEqual(len(list(trades)), 1)

            await blur.clearMessageBuffer()
            await asyncio.sleep(self.SLEEP)
            self.assertEqual(blur.messageBuffer.qsize(), 1)

        asyncio.run(test())

    def test_messageBuffer(self):
        badtx = HexBytes('0x3976f2657aca7b7f99e2345418cb4a9abc6792a157cb09b9ad3206c846dec458')
        goodtx = HexBytes('0x3976f2657aca7b7f99e2345418cb4a9abc6792a157cb09b9ad3206c846dec459')
        blur = Blur(asyncio.Queue(), self.ethNode, self.mockClient)

        goodLog = dict(self.ethNode.getLogs(self.blurTx)[-1])
        goodLog['transactionHash'] = goodtx

        badLog = dict(self.ethNode.getLogs(self.blurTx)[-1])
        badLog['transactionHash'] = badtx

        async def test():
            asyncio.create_task(blur.start())
            await blur.aq.put(badLog)

            await asyncio.sleep(self.SLEEP)

            self.assertEqual(blur.messageBuffer.qsize(), 1)

            blur.messageBuffer.queue[0]['transactionHash'] = goodtx

            await blur.aq.put(goodLog)

            await asyncio.sleep(self.SLEEP)

            self.assertEqual(blur.messageBuffer.qsize(), 0)

            trades = blur.client.trades.find()
            self.assertEqual(len(list(trades)), 2)

        asyncio.run(test())

    def test_clearMessageBuffer(self):
        log = self.ethNode.getLogs(self.blurTx)[-1]
        blur = Blur(asyncio.Queue(), self.ethNode, self.mockClient)
        log = dict(log)
        log['transactionHash'] = HexBytes('0x3976f2656aca7b7f99e2345418cb4a9abc6792a157cb09b9ad3206c846dec458')

        good = HexBytes('0x3976f2657aca7b7f99e2345418cb4a9abc6792a157cb09b9ad3206c846dec459')

        async def test():
            asyncio.create_task(blur.start())
            await blur.aq.put(log)

            await asyncio.sleep(self.SLEEP)

            self.assertEqual(blur.messageBuffer.qsize(), 1)
            self.assertEqual(blur.messageBuffer.queue[0], log)

            await blur.clearMessageBuffer()

            await asyncio.sleep(self.SLEEP)

            self.assertEqual(blur.messageBuffer.qsize(), 1)
            self.assertEqual(blur.messageBuffer.queue[0], log)

            blur.messageBuffer.queue[0]['transactionHash'] = good

            await blur.clearMessageBuffer()

            await asyncio.sleep(self.SLEEP)

            self.assertEqual(blur.messageBuffer.qsize(), 0)
            
            trades = blur.client.trades.find()
            self.assertEqual(len(list(trades)), 1)
        asyncio.run(test())

    # Test the buffer in the marketplace
    def test_buffer(self):
        log = self.ethNode.getLogs(self.blurTx)[-1]

        blur = Blur(asyncio.Queue(), self.ethNode, self.badMockClient)

        async def test():
            asyncio.create_task(blur.start())
            await blur.aq.put(log)
            await asyncio.sleep(self.SLEEP)
            self.assertEqual(blur.buffer.qsize(), 1)

            await blur.aq.put(log)
            await asyncio.sleep(self.SLEEP)
            self.assertEqual(blur.buffer.qsize(), 2)

            await blur.aq.put(log)
            await asyncio.sleep(self.SLEEP)
            self.assertEqual(blur.buffer.qsize(), 3)

            # switch to good client
            blur.client = self.mockClient 

            await blur.aq.put(log)
            await asyncio.sleep(self.SLEEP)
            self.assertEqual(blur.buffer.qsize(), 0)

            # 4 items in the database
            trades = blur.client.trades.find()
            self.assertEqual(len(list(trades)), 4)

        asyncio.run(test())
