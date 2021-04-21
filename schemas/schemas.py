from models.guest_model import Guest
from models.appointment_model import Appointment
from settings import ma
from marshmallow import validates, validate, ValidationError, fields
from marshmallow_sqlalchemy.fields import Nested


class GuestSchema(ma.SQLAlchemyAutoSchema):
    class Meta:

        model = Guest
        # include_relationships = True

    # appointments = ma.Nested(lambda: AppointmentSchema, many=True, exclude=('guest',))
        


# deze schema wordt gebruikt wanneer gegevens van een gast aangepast moeten worden
class EditGuestSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Guest

    name = fields.Str(required=False, validate=validate.Length(min=3, max=30))
    email = fields.Email(required=False)
    company = fields.Str(required=False, validate=validate.Length(min=3, max=30))
    phone_number = fields.Str(required=False, validate=validate.Length(min=8, max=15))
    license_plate = fields.Str(required=False, validate=validate.Length(min=3, max=30))
    consent_duration = fields.Int(required=False, validate=validate.Range(min=0))


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

from models.user_model import User
from settings import ma
from marshmallow import validates, validate, ValidationError, fields


def password_check(password):
    if len(password) < 3:
        raise ValidationError("password length must be greater than 3.")
    if len(password) > 30:
        raise ValidationError("password must not be greater than 30.")


# Autoschema maakt automatisch voor ieder column een field aan en voegt het toe aan de schema.
# je kan columns nog steeds zelf in schema neerzetten, dit wil je doen wanneer je extra validaties wilt toevoegen.
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

    name = fields.Str(validate=validate.Length(min=3, max=30))
    email = fields.Str(validate=validate.Length(min=3, max=30))
    password = fields.Str(validate=password_check)


# deze schema wordt gebruikt wanneer een user zijn settings aanpast,
# hier is inprincipe geen field verplicht om in te vullen.
class EditUserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

    name = fields.Str(required=False, validate=validate.Length(min=3, max=30))
    email = fields.Str(required=False, validate=validate.Length(min=3, max=30))
    password = fields.Str(required=False, validate=password_check)
    is_admin = fields.Boolean(required=False)


class EditUserPasswordSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

    name = fields.Str(required=False, validate=validate.Length(min=3, max=30))
    email = fields.Str(required=False, validate=validate.Length(min=3, max=30))
    password = fields.Str(required=True, validate=password_check)
    new_password = fields.Str(required=True, validate=password_check)
    is_admin = fields.Boolean(required=False)



