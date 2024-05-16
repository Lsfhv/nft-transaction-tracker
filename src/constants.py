from hexbytes import HexBytes
import os 
from enum import Enum

WETH = HexBytes('0xC02aaA39b223FE8D0A0e5C4F27eAD9083C756Cc2')

blur_contract_address = '0xb2ecfE4E4D61f8790bbb9DE2D1259B9e2410CEA5'
blur_taker_topic = '0x0fcf17fac114131b10f37b183c6a60f905911e52802caeeb3e6ea210398b81ab'
blur_maker_topic = '0x7dc5c0699ac8dd5250cbe368a2fc3b4a2daadb120ad07f6cccea29f83482686e'

infura_key = os.environ["INFURAAPIKEY"] 
infura_ws_endpoint = f"wss://mainnet.infura.io/ws/v3/{infura_key}"

class MarketType(Enum):
    OPENSEA = "OPENSEA"
    BLUR = "BLUR"
    MAGICEDEN = "MAGICEDEN"

class Side(Enum):
    MAKER = 0
    TAKER = 1