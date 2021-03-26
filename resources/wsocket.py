# import asyncio
# import websockets

# async def test(websocket, path):
#     # uri = "ws://localhost:8080/"
#     # async with websockets.connect(uri) as ws:
#     name = input('geef je naam')
    
#     await websocket.send(name)
#     print(name)
        
#     greeting = await websocket.recv()
#     print(greeting)
    
# start_server = websockets.serve(test, "127.0.0.1", 5678)

# asyncio.get_event_loop().run_until_complete(start_server)
# asyncio.get_event_loop().run_forever()

# # if __name__ == '__main__':
# #     main()

# # asyncio.get_event_loop().run_until_complete(test())