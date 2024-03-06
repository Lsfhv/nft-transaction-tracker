from blur import Blur 
import asyncio
from os import environ
from eth_node import EthNode

from pymongo import MongoClient

async def main():
    infuraKey = environ['INFURAAPIKEY']

    q = asyncio.Queue()
    ethNode = EthNode(infuraKey)
        
    asyncio.create_task(Blur(q, ethNode).start())
    await ethNode.ws_v2_subscription_context_manager_example(q, infuraKey)

if __name__ == "__main__":
    asyncio.run(main())
    
# infuraKey = environ['INFURAAPIKEY']
# ethNode = EthNode(infuraKey)    
# logs = ethNode.getLogs('0xd39579a60b3bc03d174c883b436e8f1d9153ce3d70b4a34aec7b2f4144e0c7db')
# log = logs[-1]
# q = asyncio.Queue()
# blur = Blur(q, ethNode)

# x = blur.decode(log)
    
# client = MongoClient('192.168.0.6', 27017)
# nft = client.nft
# print(nft.trades.insert_one(x.getDict())   )