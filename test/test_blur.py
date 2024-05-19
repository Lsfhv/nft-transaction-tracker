import unittest
from test_data import (
    BLUR_MAKER_MSG,
    BLUR_TAKER_MSG,
    BLUR_MAKER_TRADE,
    BLUR_TAKER_TRADE,
    TEST_BLUR
)


class TestBlur(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_decode_w_maker(self):
        trade = TEST_BLUR.decode(BLUR_MAKER_MSG)
        self.assertEqual(trade, BLUR_MAKER_TRADE)

    def test_decode_w_taker(self):
        trade = TEST_BLUR.decode(BLUR_TAKER_MSG)
        self.assertEqual(trade, BLUR_TAKER_TRADE)
