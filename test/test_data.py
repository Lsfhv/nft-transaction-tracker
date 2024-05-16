from hexbytes import HexBytes
from datetime import datetime 
from src.constants import MarketType, Side
from src.trade import Trade, TradeType

TX_HASH = '0x3f61ce351938a9f67acbaa41d42e3212d5895e94639e56870e909c99cacf7fa6'
TX_HASH_W_LOTS_LOGS = '0x682dcf4f1794fd19b7690dac24946a6aae4bcc6e495769adf0cfb3ee7927abce'
ADD_LEN = 42

SLEEP = 0.1

BLUR_MAKER_MSG = {'address': '0xb2ecfe4e4d61f8790bbb9de2d1259b9e2410cea5', 'blockHash': '0x137c3588e2d240cb255a0e83e3fff87a6ee50e939b553395055968ab01502c5c', 'blockNumber': '0x12f61a0', 'data': '0x28cfe965d7c7d8be78f88ea85bffe214611fe7d35b4d9ae1a52177a3512eb4db00000000000000000f429d00d2e80d60aff5377587e49ff32c9bad639d6f68bc000000000453068c90030000f9e39ce3463b8def5748ff9b8f7825af8f1b1617000000000000000000000032bb70ccc326bb0c98487cc4e281a4d7b9e1624baa', 'logIndex': '0x172', 'removed': False, 'topics': ['0x7dc5c0699ac8dd5250cbe368a2fc3b4a2daadb120ad07f6cccea29f83482686e'], 'transactionHash': '0x8cf2b6d5adb5d11fb6a9b773d524b6a40ac27d69d03dffbeba17c21b48da2466', 'transactionIndex': '0x86'}

BLUR_MAKER_TRADE = Trade(
            '0x8cf2b6d5adb5d11fb6a9b773d524b6a40ac27d69d03dffbeba17c21b48da2466',
            HexBytes('0xd2e80D60aff5377587E49FF32c9bad639d6f68Bc'), 
            HexBytes('0x6Ce922B3d81BA1e1bDD58003AD148552000a0bfA'),
            HexBytes(1000093),
            HexBytes('0xf9e39ce3463B8dEF5748Ff9B8F7825aF8F1b1617'),
            HexBytes(311600000000000000),
            0.005, 
            HexBytes('0xBB70CcC326BB0C98487cc4E281A4D7b9e1624bAA'),
            Side.MAKER,
            datetime(2024, 5, 16, 12, 0, 47), 
            MarketType.BLUR
        )

BLUR_TAKER_MSG = {'address': '0xb2ecfe4e4d61f8790bbb9de2d1259b9e2410cea5', 'blockHash': '0x28fa01ee0e247d590f4b1329399812d68a10976ed10782cc276c9b05c660b204', 'blockNumber': '0x12f65eb', 'data': '0xac96d4c120e5531f660848883aeae29bc70f7f4f4b6550a4cdf5af7be928bac1000000000000000000055900d2205aa882e005066b32764cf6748bd07bdcf78801000000016345785d8a00008fc0d90f2c45a5e7f94904075c952e0943cfccfd000000000000000000000032e68acb8a71dba532c88b8772542b5e97ce0a5001', 'logIndex': '0x2c0', 'removed': False, 'topics': ['0x0fcf17fac114131b10f37b183c6a60f905911e52802caeeb3e6ea210398b81ab'], 'transactionHash': '0x762dcd0d964512e5a44ccf0c8a8edb992af239b41549e18b4ddad32a8d647c4b', 'transactionIndex': '0xdd'}

BLUR_TAKER_TRADE = Trade(
            '0x762dcd0d964512e5a44ccf0c8a8edb992af239b41549e18b4ddad32a8d647c4b', 
            HexBytes('0xbb6712A513C2d7F3E17A40d095a773c5d98574B2'), 
            HexBytes('0xd2205AA882e005066B32764CF6748bD07BDCF788'), 
            HexBytes(1369), 
            HexBytes('0x8Fc0D90f2C45a5e7f94904075c952e0943CFCCfd'),
            HexBytes(100000000000000000), 
            0.005, 
            HexBytes('0xE68ACB8A71dba532c88b8772542b5e97cE0a5001'),
            Side.TAKER,
            datetime(2024, 5, 16, 15, 41, 35),
            MarketType.BLUR
        )

