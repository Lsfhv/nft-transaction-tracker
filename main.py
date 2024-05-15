from src.blur import Blur 
from src.opensea import Opensea
import asyncio
from os import environ
from src.eth_node import EthNode
from src.magiceden import MagicEden
from pymongo import MongoClient
import logging 

logger = logging.getLogger(__name__)

async def main():
    infuraKey = environ['INFURAAPIKEY']

    ethNode = EthNode(infuraKey)
    # client = MongoClient('192.168.0.6', 27017).nft 
    client = MongoClient('localhost', 27017).nft

    os = Opensea(asyncio.Queue(), ethNode, client)
    blur = Blur(asyncio.Queue(), ethNode, client)
    magicEden = MagicEden(asyncio.Queue(), ethNode, client)
        
    # asyncio.create_task(os.start())
    asyncio.create_task(blur.start())
    # asyncio.create_task(magicEden.start())

    await ethNode.w2Logs([blur, os, magicEden], infuraKey)

if __name__ == "__main__":
    asyncio.run(main())