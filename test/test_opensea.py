import unittest 
from test_data import (
    TEST_OPENSEA, 
    OPENSEA_SELL_MSG, 
    OPENSEA_SELL_TRADE, 
    OPENSEA_BUY_MSG, 
    OPENSEA_BUY_TRADE
)


class TestOpensea(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_decode_w_buy(self):
        trade = TEST_OPENSEA.decode(OPENSEA_BUY_MSG)
        self.assertEqual(trade, OPENSEA_BUY_TRADE)

    def test_decode_w_sell(self):
        trade = TEST_OPENSEA.decode(OPENSEA_SELL_MSG)
        self.assertEqual(trade, OPENSEA_SELL_TRADE)

        

