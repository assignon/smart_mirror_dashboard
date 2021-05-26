from flask_restful import Resource, reqparse, abort
from flask import request, jsonify, make_response
from settings import ma, db, redis_db
from sqlalchemy import exc
from sqlalchemy.orm.exc import NoResultFound
from .authentication_api import login_required
from .helper import remove_whitespace
# models imports

from models.guest_model import Guest


class RedisCache(Resource):

    @staticmethod
    @login_required
    def get(current_user):
        """
        get all cache_ids with unix time
        """
        cache_ids_with_unixtimes = redis_db.get_cache_ids_with_unixtime()
        return {"cache_ids_with_unixtime": cache_ids_with_unixtimes}

    @staticmethod
    @login_required
    def put(current_user, cache_id=None):
        """
        label the cached embeddings of specified cache
        """
        if not cache_id:
            return {"error": "cache_id is missing in path"}

        if cache_id not in redis_db.get_cache_ids():
            return {"error": "invalid cache_id!"}

        json_data: dict = request.get_json()
        if not json_data:
            return {" error": "JSON missing :("}
        if 'body' not in json_data.keys():
            return {"error": "body key missing!"}
        json_data = json_data['body']

        if 'guest_id' not in json_data.keys():
            return {"error": "guest_id is missing!"}

        try:
            guest = Guest.get_guest(json_data['guest_id'])
        except NoResultFound:
            return {"error": "Specified guest_id does not exist in the database"}

        redis_db.label_unknown_embeddings(cache_id, guest.guest_id, guest.consent_expire_date)
        return 200

    @staticmethod
    @login_required
    def delete(current_user, cache_id=None):
        """Delete specified cache"""
        if not cache_id:
            return {"error": "cache_id is missing in path"}
        redis_db.delete_unknown_cache(cache_id)
        return 200
