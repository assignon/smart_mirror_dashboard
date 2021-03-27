from settings import rest_api
# models imports
from resources.user_api import *
from resources.authentication_api import Login, Logout


def api_routes(rest_api):
    # routes map
    routes = [
        {'name': UserCollection, 'path': '/users'},
        {'name': UserApi, 'path': '/user/<int:user_id>'},
        {'name': Login, 'path': '/login'}
    ]
    # add api routes and make it accessible
    for route in routes:
        rest_api.add_resource(route['name'], route['path'])