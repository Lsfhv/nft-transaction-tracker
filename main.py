from src.blur import Blur
from src.opensea import Opensea
import asyncio
from os import environ
from src.eth_node import EthNode
from src.magiceden import MagicEden
from pymongo import MongoClient
import logging
from src.constants import MarketType
from src.websocket_client import connect_to_endpoint
from hexbytes import HexBytes   

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(filename='myapp.log', level=logging.INFO)

    logger.info('Started')

    infuraKey = environ['INFURAAPIKEY']

    ethNode = EthNode(infuraKey)
    # client = MongoClient('192.168.0.6', 27017).nft 
    client = MongoClient('localhost', 27017).nft

    # os = Opensea(asyncio.Queue(), ethNode, client)
    blur = Blur(asyncio.Queue(), ethNode, client)
    # magicEden = MagicEden(asyncio.Queue(), ethNode, client)
 
    # asyncio.create_task(os.start())
    asyncio.create_task(blur.start())
    # asyncio.create_task(magicEden.start())


    await asyncio.sleep(1)

    await connect_to_endpoint({MarketType.BLUR.value: blur})


if __name__ == "__main__":
    asyncio.run(main())
