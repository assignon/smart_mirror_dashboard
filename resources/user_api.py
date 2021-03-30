from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
# import asyncio
# import websockets
from .wsocket import Wsocket
# models imports
from models.user_model import *

model = UserModel()

# async def test(websocket, path):
#     # name = input('geef je naam')
    
#     await websocket.send('test')
        
#     greeting = await websocket.recv()
#     print(greeting)
    
class CreateUser(Resource):
    def post(self):
        pass

class GetUser(Resource):
    # @jwt_required
    def get(self):
    #    return model.get_user()
        # loop = asyncio.new_event_loop()
        # asyncio.set_event_loop(loop)
    
        # start_server = websockets.serve(test, "127.0.0.1", 5678)
        # asyncio.get_event_loop().run_until_complete(start_server)
        # asyncio.get_event_loop().run_forever()
        # wsocket = Wsocket('hallo from server')
        # wsocket.serve_ws()
        
        return 'run'