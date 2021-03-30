import asyncio
import websockets
from websockets import WebSocketServerProtocol
import random

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

# # asyncio.get_event_loop().run_until_complete(test())import asyncio

class Wsocket:
    clients = set()

    def __init__(self, msg):
        self.msg = msg

    async def register(self, ws: WebSocketServerProtocol):
        self.clients.add(ws)
        print(ws.remote_address, self.clients, 'connected')

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        print(ws.remote_address, 'unregister')

    async def send_data(self, ws: WebSocketServerProtocol, data):
        if self.clients:
            # for client in self.clients:
            #     await asyncio.wait(client.send(data))
            await ws.send(data)
            # await asyncio.wait([client.send(data) for client in self.clients])
            print('msg send')

    async def receive(self, ws: WebSocketServerProtocol):
        data_recv = await ws.recv()
        return data_recv
        # while int(data_recv) < 10:
        #     i = input('je naam')
        #     await self.send_data(ws, i)
        #     print(data_recv)

    async def ws_handler(self, ws: WebSocketServerProtocol, uri):
        # await self.register(ws)
        await self.register(ws)
        try:
            await self.send_data(ws, self.msg)
            print(await self.receive(ws))
            # await self.distribute(ws)
            print(self.clients)
        finally:
            self.unregister(ws)

    # async def distribute(self, ws: WebSocketServerProtocol):
    #     async for msg in ws:
    #         await self.send_data(msg)

    def serve_ws(self):
        # host_name = "192.168.178.192"
        # host_name_pi = "192.168.178.192"
        host_name = '127.0.0.1'
        try:
            start_server = websockets.serve(
                self.ws_handler, host_name, 5678)
            asyncio.get_event_loop().run_until_complete(start_server)
            asyncio.get_event_loop().run_forever()
        except RuntimeError as ex:
            # if "There is no current event loop in thread" in str(ex):
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            start_server = websockets.serve(
                self.ws_handler, host_name, 5678)
            asyncio.get_event_loop().run_until_complete(start_server)
            asyncio.get_event_loop().run_forever()

        # start_server = websockets.serve(self.ws_handler, host_name, 5678)
        # asyncio.get_event_loop().run_until_complete(start_server)
        # asyncio.get_event_loop().run_forever()
        
# names = ['Harry', 'John', 'Smith', 'Larry']
# print(random.choice(names))
# wsocket = Wsocket('hallo from server {}'.format(random.choice(names)))
# wsocket.serve_ws()