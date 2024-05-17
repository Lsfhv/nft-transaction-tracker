import unittest 
from src.blur import Blur 
from src.eth_node import EthNode 
from os import environ
import asyncio
from test_data import BLUR_MAKER_MSG, BLUR_TAKER_MSG, BLUR_MAKER_TRADE, BLUR_TAKER_TRADE

class TestBlur(unittest.TestCase):
    def setUp(self) -> None:
        infuraKey = environ['INFURAAPIKEY']
        self.ethNode = EthNode(infuraKey)
        self.blur = Blur(asyncio.Queue(), self.ethNode, None)

    def test_decode_w_maker(self):
        trade = self.blur.decode(BLUR_MAKER_MSG)
        self.assertEqual(trade, BLUR_MAKER_TRADE)

    def test_decode_w_taker(self):  
        trade = self.blur.decode(BLUR_TAKER_MSG)
        self.assertEqual(trade, BLUR_TAKER_TRADE)

    def test_db_representation(self):        
        # getting db representation of trade doesn't throw an error
        trade_for_db = self.blur.decode(BLUR_MAKER_MSG).get_trade_for_db()

# python3 -m unittest discover test '*.py' 
        