from models.appointment_model import Appointment
from settings import ma
from marshmallow import validates, validate, ValidationError, fields


class AppointmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Appointment
        include_fk = True


# deze schema wordt gebruikt wanneer gegevens van een appointment aangepast moeten worden
class EditAppointmentSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Appointment
        include_fk = True

    guest_id = fields.Int(required=False)
