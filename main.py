from src.blur import Blur
from src.opensea import Opensea
import asyncio
from os import environ
from src.eth_node import EthNode
from src.magiceden import MagicEden
from pymongo import MongoClient
import logging
from src.constants import MarketType, LOG_FILENAME
from src.websocket_client import connect_to_endpoint
from hexbytes import HexBytes
from web3.datastructures import AttributeDict
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)


async def start_marketplaces(eth_node: EthNode, db_client: MongoClient):
    blur = Blur(asyncio.Queue(), eth_node, db_client)
    magicEden = MagicEden(asyncio.Queue(), eth_node, db_client)
    os = Opensea(asyncio.Queue(), eth_node, db_client)

    asyncio.create_task(blur.start())
    asyncio.create_task(magicEden.start())
    asyncio.create_task(os.start())

    return blur, magicEden, os


def setup_logger():
    log_handler = RotatingFileHandler(LOG_FILENAME, maxBytes=10 * 1024 * 1024, backupCount=10)
    logging.basicConfig(handlers=[log_handler], level=logging.INFO)


async def main():
    setup_logger()

    infura_key = environ['INFURAAPIKEY']

    eth_node = EthNode(infura_key)
    # client = MongoClient('192.168.0.6', 27017).nft 
    client = MongoClient('localhost', 27017).nft

    blur, magic_eden, os = await start_marketplaces(eth_node, client)

    await asyncio.sleep(1)

    await connect_to_endpoint({MarketType.BLUR.value: blur,
                               MarketType.MAGICEDEN.value: magic_eden,
                               MarketType.OPENSEA.value: os})


if __name__ == "__main__":
    asyncio.run(main())

# infura_key = environ['INFURAAPIKEY']
# eth_node = EthNode(infura_key)
# me = MagicEden(asyncio.Queue(), eth_node, None)
# logs = eth_node.getLogs('0xca47e2e33fdbc54dfc4d294c5c1ecc83d94ff4e1a659b49fe11f7b80d1b370c3')[2]
# # print(logs)
# # me.decode(logs)

# MAGICEDEN_BUY_MSG = {'address': '0x9a1d00bed7cd04bcda516d721a596eb22aac6834', 'blockHash': '0xfe4ba668ad5d83045cf339d6a7c631a0e9967570db2868f69348abcd0dfc2c77', 'blockNumber': '0x12f7c19', 'data': '0x00000000000000000000000067dda6b2d5f65e9948df89ed9dfe99ecaee96f6700000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000d510000000000000000000000000000000000000000000000001c7310237d8d0000', 'logIndex': '0x53', 'removed': False, 'topics': ['0xffb29e9cf48456d56b6d414855b66a7ec060ce2054dcb124a1876310e1b7355c', '0x00000000000000000000000067dda6b2d5f65e9948df89ed9dfe99ecaee96f67', '0x0000000000000000000000005d3f81ad171616571bf3119a3120e392b914fd7c', '0x0000000000000000000000008821bee2ba0df28761afff119d66390d594cd280'], 'transactionHash': '0xca47e2e33fdbc54dfc4d294c5c1ecc83d94ff4e1a659b49fe11f7b80d1b370c3', 'transactionIndex': '0x36'}
# # MAGICEDEN_BUY_MSG['data'] = HexBytes(MAGICEDEN_BUY_MSG['data'])
# MAGICEDEN_BUY_MSG['topics'] = [HexBytes(i) for i in MAGICEDEN_BUY_MSG['topics']]
# # MAGICEDEN_BUY_MSG['transactionHash'] = HexBytes(MAGICEDEN_BUY_MSG['transactionHash'])
# x = AttributeDict(MAGICEDEN_BUY_MSG)

# print(me.decode(x))
# def convert(logs):
#     result = dict(logs)
#     result['transactionHash'] = result['transactionHash'].hex() 
#     result['data'] = result['data'].hex()
#     for i in range(len(result['topics'])):
#         result['topics'][i] = result['topics'][i].hex()
#     return result
