import websockets
from src.marketplace import Marketplace
import json
import logging
from hexbytes import HexBytes

from src.constants import (
    BLUR_CONTRACT_ADDRESS,
    BLUR_TAKER_TOPIC,
    BLUR_MAKER_TOPIC,
    INFURA_WS_ENDPOINT,
    MAGICEDEN_BUY_LISTING_ERC721_TOPIC, 
    MAGICEDEN_ACCEPT_OFFER_ERC721_TOPIC, 
    MAGICEDEN_CONTRACT_ADDRESS, 
    MarketType,
    OPENSEA_1_6_CONTRACT_ADDRESS,   
    OPENSEA_ORDER_FULFILLED_TOPIC,
)

logger = logging.getLogger(__name__)    


def create_eth_log_subscription_request(address: str, topic: str, id) -> str:
    return json.dumps({
        "jsonrpc": "2.0",
        "id": id,
        "method": "eth_subscribe",
        "params": ["logs", {"address": address, "topics": [topic]}]
    })


async def connect_to_endpoint(market_places: dict[MarketType, Marketplace]):
    logger.info('Connecting to websocket endpoint')
    ws = await websockets.connect(INFURA_WS_ENDPOINT, ping_interval=None)

    sub_map = {}

    await ws.send(create_eth_log_subscription_request(BLUR_CONTRACT_ADDRESS, BLUR_TAKER_TOPIC, BLUR_TAKER_TOPIC))
    await ws.send(create_eth_log_subscription_request(BLUR_CONTRACT_ADDRESS, BLUR_MAKER_TOPIC, BLUR_MAKER_TOPIC))

    await ws.send(create_eth_log_subscription_request(
        MAGICEDEN_CONTRACT_ADDRESS, 
        MAGICEDEN_BUY_LISTING_ERC721_TOPIC,
        MAGICEDEN_BUY_LISTING_ERC721_TOPIC
    ))

    await ws.send(create_eth_log_subscription_request(
        MAGICEDEN_CONTRACT_ADDRESS, 
        MAGICEDEN_ACCEPT_OFFER_ERC721_TOPIC,
        MAGICEDEN_ACCEPT_OFFER_ERC721_TOPIC
    ))

    await ws.send(create_eth_log_subscription_request(
        OPENSEA_1_6_CONTRACT_ADDRESS,
        OPENSEA_ORDER_FULFILLED_TOPIC,
        OPENSEA_ORDER_FULFILLED_TOPIC
    ))

    sub_map[BLUR_TAKER_TOPIC] = market_places[MarketType.BLUR.value]
    sub_map[BLUR_MAKER_TOPIC] = market_places[MarketType.BLUR.value]

    sub_map[MAGICEDEN_BUY_LISTING_ERC721_TOPIC] = market_places[MarketType.MAGICEDEN.value]
    sub_map[MAGICEDEN_ACCEPT_OFFER_ERC721_TOPIC] = market_places[MarketType.MAGICEDEN.value]

    sub_map[OPENSEA_ORDER_FULFILLED_TOPIC] = market_places[MarketType.OPENSEA.value]

    while True:
        response = json.loads(await ws.recv())

        if "result" in response:

            marketplace = sub_map[response['id']]
            sub_map[response['result']] = marketplace

            logger.info(f"Subscribed to {marketplace.__class__.__name__}")
        else:
            
            sub = response['params']['subscription']
            msg = response['params']['result']

            marketplace = sub_map[sub]
            await marketplace.aq.put(msg)

