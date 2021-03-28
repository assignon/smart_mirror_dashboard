from flask_restful import Resource, reqparse, abort
from flask import request, jsonify, make_response
from settings import ma, db
from marshmallow import ValidationError
from sqlalchemy import exc
from sqlalchemy.orm.exc import NoResultFound
from .authentication_api import login_required
from schemas.appointment_schema import AppointmentSchema, EditAppointmentSchema
from models.appointment_model import Appointment


appointment_schema = AppointmentSchema()
appointments_schema = AppointmentSchema(many=True)
edit_appointment_schema = EditAppointmentSchema()


class AppointmentCollection(Resource):
    
    @staticmethod
    @login_required
    def get():
        """
        nog niet zeker wat dit moet gaan doen
        """
        pass

    @staticmethod
    @login_required
    def post(current_user):
        """
        Creates a new appointment in the appointment table
        """
        json_data = request.get_json()
        if not json_data:
            return {"message": "No input data provided"}, 400
        
        # remove whitespaces from input
        
        remove_whitespace(json_data)

        # Validate and deserialize input
        
        try:
            data = appointment_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422
        
        try: 
            appointment = Appointment.create(**data)
        except exc.IntegrityError as e:
            db.session.rollback()
            return{'error': e.orig.args}
        
        return appointment_schema.dump(appointment), 201
    
    
    @staticmethod
    @login_required
    def delete(current_user, appoinment_id):
        Appointment.delete_appointment(appoinment_id)
        return 200


class AppointmentApi(Resource):
    

    @staticmethod
    @login_required
    def put(current_user, appoinment_id):

        json_data = request.get_json()

        if not json_data:
            return {"message": "No input data provided"}, 400
        
        # remove whitespaces from input
        
        remove_whitespace(json_data)

        # Validate and deserialize input
        
        try:
            data = edit_appointment_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422

        try:        
            edited_appointment = Appointment.update_guest(appoinment_id, **data)
        except exc.IntegrityError as e:
            db.session.rollback()
            return{'error': e.orig.args}
        except NoResultFound:
            return{'error': 'Guest does not exist'}

        return appointment_schema.dump(edited_appointment), 200

def remove_whitespace(json_data):
    for key, value in json_data.items():
        if type(value) == str:
            json_data[key] = value.strip()