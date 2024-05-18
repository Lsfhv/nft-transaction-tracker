import unittest 
from test_data import (
    TEST_MAGICEDEN, 
    MAGICEDEN_BUY_MSG, 
    MAGICEDEN_BUY_TRADE, 
    MAGICEDEN_SELL_MSG,
    MAGICEDEN_SELL_TRADE
)


class TestMagicEden(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_decode_w_buy(self):
        trade = TEST_MAGICEDEN.decode(MAGICEDEN_BUY_MSG)
        self.assertEqual(trade, MAGICEDEN_BUY_TRADE)    

    def test_decode_w_sell(self):  
        trade = TEST_MAGICEDEN.decode(MAGICEDEN_SELL_MSG)
        self.assertEqual(trade, MAGICEDEN_SELL_TRADE)
    

