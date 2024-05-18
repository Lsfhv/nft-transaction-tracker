# from web3 import Web3, AsyncWeb3
# from web3.providers import WebsocketProviderV2
# import asyncio
# from src.constants import blur_contract_address, blur_taker_topic, blur_maker_topic
# import websockets

# async def ws_v2_subscription_context_manager_example():
#     print("started")
#     async with AsyncWeb3.persistent_websocket(
#         WebsocketProviderV2(f"wss://mainnet.infura.io/ws/v3/b733902d9de349448dd8a88304ae04cb"), 
        
#     ) as w3:
#         # subscribe to new block headers
#         # subscription_id = await w3.eth.subscribe("newHeads")

        

#         await w3.eth.subscribe("logs", {
#                     "address": blur_contract_address,
#                     "topics": [blur_taker_topic]
#                     }) 
        
#         await w3.eth.subscribe("logs", {


#                 "address": blur_contract_address,
#                 "topics": [blur_maker_topic]
#                 }) 

#         count = 0
#         async for response in w3.ws.process_subscriptions():
#             print(f"{response}\n")
#             # handle responses here
#             count += 1
#             print(f"Count: {count}")
#             # if some_condition:
#             #     # unsubscribe from new block headers and break out of
#             #     # iterator
#             #     await w3.eth.unsubscribe(subscription_id)
#             #     break

#         # still an open connection, make any other requests and get
#         # responses via send / receive
#         latest_block = await w3.eth.get_block("latest")
#         print(f"Latest block: {latest_block}")

#         # the connection closes automatically when exiting the context
#         # manager (the `async with` block)

# async def atest():
#     print("started")
#     websocket = await websockets.connect("wss://mainnet.infura.io/ws/v3/b733902d9de349448dd8a88304ae04cb", ping_interval=None)

#     await websocket.send('{"jsonrpc":"2.0", "id": 1, "method": "eth_subscribe", "params": ["logs", {"address": "0xb2ecfE4E4D61f8790bbb9DE2D1259B9e2410CEA5", "topics":["0x0fcf17fac114131b10f37b183c6a60f905911e52802caeeb3e6ea210398b81ab"]}]}')
#     await websocket.send('{"jsonrpc":"2.0", "id": 1, "method": "eth_subscribe", "params": ["logs", {"address": "0xb2ecfE4E4D61f8790bbb9DE2D1259B9e2410CEA5", "topics":["0x7dc5c0699ac8dd5250cbe368a2fc3b4a2daadb120ad07f6cccea29f83482686e"]}]}')
#     while True:
#         response = await websocket.recv()
#         print(f"{response}")  



# if __name__ == "__main__":
#     asyncio.run(atest())