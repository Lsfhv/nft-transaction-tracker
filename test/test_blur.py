import unittest 
from src.blur import Blur 
from src.eth_node import EthNode 
from os import environ
import asyncio
from hexbytes import HexBytes
from src.trade import TradeType

class TestBlur(unittest.TestCase):
    def setUp(self) -> None:
        infuraKey = environ['INFURAAPIKEY']
        self.ethNode = EthNode(infuraKey)
        self.blur = Blur(asyncio.Queue(), self.ethNode, None)

        self.rhb = lambda x : HexBytes(int(x.hex(), 16))

        self.addressLength = 42

    def asrtAddLen(self, result):
        self.assertEqual(len(result.source.hex()), self.addressLength)
        self.assertEqual(len(result.destination.hex()), self.addressLength)
        self.assertEqual(len(result.collectionAddress.hex()), self.addressLength)
        self.assertEqual(len(result.feeAddress.hex()), self.addressLength)
        
    def test_decode_maker(self):
        txHash = '0x9528067c2fb6b9e3cf4a851c99db0a91ccd537526d40f8c2c226adeba5a084aa'
        log = self.ethNode.getLogs(txHash)[-1]
        result = self.blur.decode(log)

        self.assertEqual(result.txHash, HexBytes('0x9528067c2fb6b9e3cf4a851c99db0a91ccd537526d40f8c2c226adeba5a084aa'))
        self.assertEqual(result.source, HexBytes('0xa331172edafbDd58a66689dA6203597d2AefE316'))
        self.assertEqual(result.destination, HexBytes('0x52c946C93798e3A47A7888164dbc0375D081F720'))
        self.assertEqual(self.rhb(result.tokenId), HexBytes(6175))
        self.assertEqual(result.collectionAddress, HexBytes('0x1A92f7381B9F03921564a437210bB9396471050C'))
        self.assertEqual(self.rhb(result.price), HexBytes(int(0.89 * 10**18)))
        self.assertEqual(result.tradeType, TradeType.MAKER)
        self.assertEqual(self.rhb(result.feeRate), HexBytes(int(0.05 * 10 ** 4)))
        self.assertEqual(result.feeAddress, HexBytes('0xD98D29Beb788fF04e7a648775FcB083282aE9C4B'))

        self.asrtAddLen(result)

    def test_decode_taker(self):
        txHash = '0x96181900db1bd33db6110ddde7b7834d11e01470e7dec76d34e1fd2e3fc25e0b'
        log = self.ethNode.getLogs(txHash)[-1]
        result = self.blur.decode(log)
        
        self.assertEqual(result.txHash, HexBytes('0x96181900db1bd33db6110ddde7b7834d11e01470e7dec76d34e1fd2e3fc25e0b'))
        self.assertEqual(result.source, HexBytes('0xA3b3ACF61034cCD05f204e24E5935ceA4d291065'))
        self.assertEqual(result.destination, HexBytes('0x319487E1BD858d73301a85E43E095cDD79741D34'))
        self.assertEqual(self.rhb(result.tokenId), HexBytes(4817))
        self.assertEqual(result.collectionAddress, HexBytes('0x1D20A51F088492A0f1C57f047A9e30c9aB5C07Ea'))  
        self.assertEqual(self.rhb(result.price), HexBytes(int(0.8 * 10**18)))
        self.assertEqual(self.rhb(result.feeRate), HexBytes(int(0.005 * 10 ** 4)))
        self.assertEqual(result.feeAddress, HexBytes('0x9906de9e0d9ef5960d02df2261ecaa78ec8ce45d'))
        self.assertEqual(result.tradeType, TradeType.TAKER)

        self.asrtAddLen(result)

    def test_decode_taker_padded_zero(self):
        txHash = '0x1d6c29ac06fb3f0a6ffd7dd580726d64bbddffdc6dfd95fdce4f60a10140c812'
        log = self.ethNode.getLogs(txHash)[4]
        result = self.blur.decode(log)

        self.assertEqual(result.source, HexBytes('0x00652700cb56bd11a52fcfb5709f89b70a445208'))
        self.assertEqual(result.destination, HexBytes('0x1e2ab2c1ee48aa5c705e6a638087bf7fc1877095'))

        self.asrtAddLen(result)

# python3 -m unittest discover test '*.py' 
        