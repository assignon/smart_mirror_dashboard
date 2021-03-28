from models.guest_model import Guest
from settings import ma
from marshmallow import validates, validate, ValidationError, fields


class GuestSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Guest



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


