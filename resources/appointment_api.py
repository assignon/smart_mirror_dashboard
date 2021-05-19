from flask_restful import Resource, reqparse, abort
from flask import request, jsonify, make_response
from settings import ma, db
from marshmallow import ValidationError
from sqlalchemy import exc
from sqlalchemy.orm.exc import NoResultFound
from .authentication_api import login_required
from schemas.schemas import AppointmentSchema, EditAppointmentSchema, CreateAppointmentSchema
from models.appointment_model import Appointment
from .helper import remove_whitespace
import datetime

appointment_schema = AppointmentSchema()
appointments_schema = AppointmentSchema(many=True)
create_appointment_schema = CreateAppointmentSchema()
edit_appointment_schema = EditAppointmentSchema()


class AppointmentCollection(Resource):

    @staticmethod
    @login_required
    def get(current_user):
        """
        Haalt alle appointments op waarvan de checkout NULL is
        """
        appointments = Appointment.get_open_appointments()
        return {"appointments": appointments_schema.dump(appointments)}

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
            data = create_appointment_schema.load(json_data)
        except ValidationError as err:
            return err.messages, 422

        try:
            appointment = Appointment.create(**data)
        except exc.IntegrityError as e:
            db.session.rollback()
            return {'error': e.orig.args}

        return {"appointment": appointment_schema.dump(appointment)}, 201

    @staticmethod
    @login_required
    def delete(current_user, appoinment_id):
        Appointment.delete_appointment(appoinment_id)
        return 200


class AppointmentApi(Resource):

    @staticmethod
    @login_required
    def put(current_user, appointment_id):
        from app import socketio

        json_data = request.get_json()
        now = datetime.datetime.now()
        print('json_dataaaaaaaa', json_data['body'])

        if not json_data:
            return {"message": "No input data provided"}, 400

        # remove whitespaces from input

        remove_whitespace(json_data)
        try:
            if json_data['body']['checked_in']:
                json_data['body']['checked_in'] = now.strftime("%Y-%m-%d %H:%M:%S")
            elif json_data['body']['checked_out']:
                json_data['body']['checked_out'] = now.strftime("%Y-%m-%d %H:%M:%S")
        except KeyError as e:
            try:
                json_data['body']['checked_out'] = now.strftime("%Y-%m-%d %H:%M:%S")
            except KeyError as e:
                print('errorrr',e)
                pass
 
        # Validate and deserialize input

        try:
            data = edit_appointment_schema.load(json_data['body'])
            
        except ValidationError as err:
            return err.messages, 422

        try:
            edited_appointment = Appointment.update_appointment(appointment_id, **data)
            # broadcast the update to all screens
            # socketio.emit('checked',  now.strftime("%Y-%m-%d %H:%M:%S"),
            #             broadcast=True)
        except exc.IntegrityError as e:
            db.session.rollback()
            return {'error': e.orig.args}
        except NoResultFound:
            return {'error': 'Appointment does not exist'}
        
        return {'appointment': appointment_schema.dump(edited_appointment)}, 200
