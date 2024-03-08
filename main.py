from src.blur import Blur 
from src.opensea import Opensea
import asyncio
from os import environ
from src.eth_node import EthNode

from pymongo import MongoClient

async def main():
    infuraKey = environ['INFURAAPIKEY']

    q = asyncio.Queue()
    ethNode = EthNode(infuraKey)
    client = MongoClient('192.168.0.6', 27017).nft 

    os = Opensea(asyncio.Queue(), ethNode, client)
    blur = Blur(asyncio.Queue(), ethNode, client)
        
    asyncio.create_task(os.start())
    asyncio.create_task(blur.start())
    await ethNode.w2Logs([blur, os], infuraKey)

if __name__ == "__main__":
    asyncio.run(main())

infuraKey = environ['INFURAAPIKEY']
ethNode = EthNode(infuraKey)    
os = Opensea(None, ethNode, None)
logs = ethNode.getLogs('0x1ec12403a0d4cafd831bd1952ee47a7dac066402366d39a3426a26a414cf3b51')
log = logs[-1]
# q = asyncio.Queue()
# blur = Blur(q, ethNode, None)

# x = blur.decode(log)
    
# client = MongoClient('192.168.0.6', 27017)
# nft = client.nft
# print(nft.trades.insert_one(x.getDict()))