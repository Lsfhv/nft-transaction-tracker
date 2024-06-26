from hexbytes import HexBytes
import os 
from enum import Enum

WETH_CONTRACT_ADDRESS = HexBytes('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2')

OPENSEA_1_6_CONTRACT_ADDRESS = '0x0000000000000068F116a894984e2DB1123eB395' 
OPENSEA_ORDER_FULFILLED_TOPIC = '0x9d9af8e38d66c62e2c12f0225249fd9d721c54b83f48d9352c97c6cacdcb6f31'

BLUR_CONTRACT_ADDRESS = '0xb2ecfE4E4D61f8790bbb9DE2D1259B9e2410CEA5'
BLUR_TAKER_TOPIC = '0x0fcf17fac114131b10f37b183c6a60f905911e52802caeeb3e6ea210398b81ab'
BLUR_MAKER_TOPIC = '0x7dc5c0699ac8dd5250cbe368a2fc3b4a2daadb120ad07f6cccea29f83482686e'

INFURA_KEY = os.environ["INFURAAPIKEY"] 
INFURA_WS_ENDPOINT = f"wss://mainnet.infura.io/ws/v3/{INFURA_KEY}"

MAGICEDEN_CONTRACT_ADDRESS = '0x9A1D00bEd7CD04BCDA516d721A596eb22Aac6834'
MAGICEDEN_ACCEPT_OFFER_ERC721_TOPIC = '0x8b87c0b049fe52718fe6ff466b514c5a93c405fb0de8fbd761a23483f9f9e198'
MAGICEDEN_BUY_LISTING_ERC721_TOPIC = '0xffb29e9cf48456d56b6d414855b66a7ec060ce2054dcb124a1876310e1b7355c'

LOG_FILENAME = 'myapp.log'

class MarketType(Enum):
    OPENSEA = "OPENSEA"
    BLUR = "BLUR"
    MAGICEDEN = "MAGICEDEN"

class SIDE(Enum):
    BUY = 0 # Someone bought a listing
    SELL = 1 # Someone accepted a bid

class TOKEN_TYPE(Enum):
    ERC721 = 0
    ERC1155 = 1
    WETH = 2
    BETH = 3
    ETH = 4
    UNKNOWN = 5