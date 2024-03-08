import unittest 
from src.marketplace import Marketplace
from hexbytes import HexBytes


class TestMarketplace(unittest.TestCase):
    def setUp(self):

        class TempMarketplace(Marketplace):
            def decode(self, message: dict):
                pass

        self.marketplace = TempMarketplace(None, None, None)


    def test_padAddress(self):
        self.assertEqual(self.marketplace.padAddress(HexBytes('0x1')), HexBytes('0x' + '0' * 39 + '1'))