from models.guest_model import Guest
from models.appointment_model import Appointment
from settings import ma
from marshmallow import validate, fields


class GuestSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Guest
        # include_relationships = True

    appointments = ma.Nested(lambda: AppointmentSchema, many=True, exclude=('guest',))


# deze schema wordt gebruikt wanneer gegevens van een gast aangepast moeten worden
class EditGuestSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Guest

    name = fields.Str(required=False, validate=validate.Length(min=3, max=30))
    email = fields.Email(required=False)
    company = fields.Str(required=False, validate=validate.Length(min=3, max=30))
    phone_number = fields.Str(required=False, validate=validate.Length(min=8, max=15))
    license_plate = fields.Str(required=False, validate=validate.Length(min=3, max=30))
    consent_expire_date = fields.Int(required=False, validate=validate.Range(min=0))


class AppointmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Appointment
        include_relationships = True

    guest = ma.Nested(GuestSchema)


# deze schema wordt gebruikt wanneer gegevens van een appointment aangepast moeten worden
class EditAppointmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Appointment

    checked_in = fields.DateTime(required=False)
    checked_out = fields.DateTime(required=False)
    has_pass = fields.Boolean(required=False)
    employee_name = fields.Str(required=False)


class CreateAppointmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Appointment

    checked_in = fields.DateTime(required=False)
    checked_out = fields.DateTime(required=False)
    has_pass = fields.Boolean(required=False)
    employee_name = fields.Str(required=True)
    guest_id = fields.Int(required=True)