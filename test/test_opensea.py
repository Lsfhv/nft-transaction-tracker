import unittest 
from os import environ 
import asyncio
from src.eth_node import EthNode
from src.opensea import Opensea
from hexbytes import HexBytes
from src.trade import TradeType, MarketType


# class TestOpensea(unittest.TestCase):
#     def setUp(self) -> None:
#         infuraKey = environ['INFURAAPIKEY']
#         self.ethNode = EthNode(infuraKey)
#         self.opensea = Opensea(asyncio.Queue(), self.ethNode, None)

#     def test_taker(self):
#         txHash = '0xd06fdf7afe129ce53e222d278384c4297b77d88c058cf8e74709e9b8e970efcc'
#         log = self.ethNode.getLogs(txHash)[0]

#         result = self.opensea.decode(log)

#         self.assertEqual(result.txHash, HexBytes('0xd06fdf7afe129ce53e222d278384c4297b77d88c058cf8e74709e9b8e970efcc'))
#         self.assertEqual(result.source, HexBytes('0xd0bc13738D982F06399844480990a5Cf59B51867'))
#         self.assertEqual(result.destination, HexBytes('0xA12611879f7e1931b56d4a31E0FA2939678643e1'))
#         self.assertEqual(result.collectionAddress, HexBytes('0x1A92f7381B9F03921564a437210bB9396471050C'))
#         self.assertEqual(result.price, HexBytes(int(2.65 * 10 ** 18)))
#         self.assertEqual(result.feeRate, HexBytes(50))
#         self.assertEqual(result.tradeType, TradeType.TAKER)
#         self.assertEqual(result.market, MarketType.OPENSEA)

#     def test_maker(self):
#         txHash = '0xa26eea60dcf3489a6f236bb764487a1050057311d6b07b41d02d8c623156b1f9'
#         log = self.ethNode.getLogs(txHash)[-1]

#         result = self.opensea.decode(log)

#         self.assertEqual(result.txHash, HexBytes('0xa26eea60dcf3489a6f236bb764487a1050057311d6b07b41d02d8c623156b1f9'))
#         self.assertEqual(result.source, HexBytes('0xc2079e5B077eae969dBEcA3747BB855Ae9DF8f3F')) 
#         self.assertEqual(result.destination, HexBytes('0x0b4648Ea410f0a907107dd61b72b447DFefc0C10'))
#         self.assertEqual(result.collectionAddress, HexBytes('0x1A92f7381B9F03921564a437210bB9396471050C'))
#         self.assertEqual(result.price, HexBytes(int(0.5 * 10 ** 18)))
#         self.assertEqual(result.feeRate, HexBytes(750))
#         self.assertEqual(result.tradeType, TradeType.MAKER)
#         self.assertEqual(result.market, MarketType.OPENSEA)

        

