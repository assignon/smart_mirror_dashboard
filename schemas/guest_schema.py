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

