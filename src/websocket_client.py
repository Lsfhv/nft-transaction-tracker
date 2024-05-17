import websockets
from src.marketplace import Marketplace
import json
import logging
from hexbytes import HexBytes

from src.constants import (
    blur_contract_address,
    blur_taker_topic,
    blur_maker_topic,
    infura_ws_endpoint,
    MAGICEDEN_BUY_LISTING_ERC721_TOPIC, 
    MAGICEDEN_ACCEPT_OFFER_ERC721_TOPIC, 
    MAGICEDEN_CONTRACT_ADDRESS, 
    MarketType
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
    ws = await websockets.connect(infura_ws_endpoint, ping_interval=None)

    sub_map = {}

    await ws.send(create_eth_log_subscription_request(blur_contract_address, blur_taker_topic, blur_taker_topic))
    await ws.send(create_eth_log_subscription_request(blur_contract_address, blur_maker_topic, blur_maker_topic))

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

    sub_map[blur_taker_topic] = market_places[MarketType.BLUR.value]
    sub_map[blur_maker_topic] = market_places[MarketType.BLUR.value]

    sub_map[MAGICEDEN_BUY_LISTING_ERC721_TOPIC] = market_places[MarketType.MAGICEDEN.value]
    sub_map[MAGICEDEN_ACCEPT_OFFER_ERC721_TOPIC] = market_places[MarketType.MAGICEDEN.value]

    while True:
        response = json.loads(await ws.recv())

        if "result" in response:

            marketplace = sub_map[response['id']]
            sub_map[response['result']] = marketplace
        else:
            
            sub = response['params']['subscription']
            msg = response['params']['result']

            marketplace = sub_map[sub]
            await marketplace.aq.put(msg)

