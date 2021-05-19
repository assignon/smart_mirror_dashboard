from flask_restful import Resource, reqparse, abort
from flask import request, jsonify, make_response
from settings import ma, db
from marshmallow import ValidationError
from sqlalchemy import exc
from sqlalchemy.orm.exc import NoResultFound
from .authentication_api import login_required
from .helper import remove_whitespace
# models imports

from models.guest_model import Guest

# schema imports
from schemas.schemas import GuestSchema, EditGuestSchema
# from schemas.guest_schema import GuestSchema, EditGuestSchema

guest_schema = GuestSchema()
guests_schema = GuestSchema(many=True)
edit_guest_schema = EditGuestSchema()


class GuestCollection(Resource):

    @staticmethod
    @login_required
    def get(current_user):
        """
        get all guests
        """
        guests = Guest.query.all()
        return {'guests': guests_schema.dump(guests)}, 200

    @staticmethod
    @login_required
    def post(current_user):
        """
        add a new guest
        """
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400

        # remove whitespaces from input

        remove_whitespace(json_data)

        # Validate and deserialize input

        try:
            data = guest_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422
        try:
            guest = Guest.create(**data)
        except exc.IntegrityError as e:
            db.session.rollback()
            return {'error': e.orig.args}

        return guest_schema.dump(guest), 201

    @staticmethod
    @login_required
    def delete(current_user, guest_id):
        Guest.delete_guest(guest_id)
        return 200


class GuestScanned(Resource):
    # @jwt_required
    """
    get result data from desktop app when guest scanned

    Args:
        Resource (api obj): [flask rest api object]
    """
    def get(self):
        from app import socketio
        # get data sended from mirror after scan
        data = request.args
        # send scan data to frontend
        try:
            print(data)
            socketio.emit('face_scanned',  data, broadcast=True)
        except  Exception as e:
            print('exxxceepttiiooonn', e)
            return {"emited": False, 'msg': 'Lijk erop dat u uitgelogd bent'}
        
        return {"emited": True, 'msg': 'Data verzonden'}
    
class GuestApi(Resource):

    @staticmethod
    @login_required
    def get(current_user, guest_id):
        """
        get specific guest
        """
        try:
            guest = Guest.get_guest(guest_id)
        except NoResultFound:
            return {'message': 'Guest does not exist!'}

        return {'guest': guest_schema.dump(guest)}, 200

    @staticmethod
    @login_required
    def put(current_user, guest_id):
        """
        edit guest
        """

        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400

        # remove whitespaces from input

        remove_whitespace(json_data)

        # Validate and deserialize input

        try:
            data = edit_guest_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422

        try:
            edited_guest = Guest.update_guest(guest_id, **data)
        except exc.IntegrityError as e:
            db.session.rollback()
            return {'error': e.orig.args}
        except NoResultFound:
            return {'error': 'Guest does not exist'}

        return {'guest': guest_schema.dump(edited_guest)}, 200
