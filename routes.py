from settings import rest_api
# models imports
from resources.user_api import *


def api_routes(rest_api):
    # routes map
    routes = [
        {'name': UserCollection, 'path': '/users'},
        {'name': UserApi, 'path': '/user/<int:user_id>'},
    ]
    # add api routes and make it accessible
    for route in routes:
        rest_api.add_resource(route['name'], route['path'])