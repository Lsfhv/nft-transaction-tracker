from src.blur import Blur
from src.opensea import Opensea
import asyncio
from os import environ
from src.eth_node import EthNode
from src.magiceden import MagicEden
from pymongo import MongoClient
import logging
from src.constants import MarketType, LOG_FILENAME, MONGODB_IP, MONGODB_PORT, INFURA_KEY
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
    log_handler = RotatingFileHandler(LOG_FILENAME, maxBytes=10 * 1024 * 1024, backupCount=20)
    formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s: %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
    log_handler.setFormatter(formatter)
    logging.basicConfig(handlers=[log_handler], level=logging.INFO)



async def main():
    setup_logger()
    eth_node = EthNode(INFURA_KEY)
    client = MongoClient(MONGODB_IP, MONGODB_PORT).nft
    blur, magic_eden, os = await start_marketplaces(eth_node, client)
    await asyncio.sleep(1)
    await connect_to_endpoint({MarketType.BLUR.value: blur,
                               MarketType.MAGICEDEN.value: magic_eden,
                               MarketType.OPENSEA.value: os})


if __name__ == "__main__":
    asyncio.run(main())