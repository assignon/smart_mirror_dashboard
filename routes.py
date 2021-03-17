# from flask_restful import Api
# import app

# models imports
from resources.user_api import *

# initialize restful api with flask app
# rest_api = Api(app)
def api_routes(rest_api):
    # routes map
    routes = [
        {'name': GetUser, 'path': '/user/get_user'}
    ]
    # add api routes and make it accessible
    for route in routes:
        rest_api.add_resource(route['name'], route['path'])