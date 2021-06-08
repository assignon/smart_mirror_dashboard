from models.user_model import User
from settings import ma
from marshmallow import validate, ValidationError, fields


def password_check(password):
    if len(password) < 3:
        raise ValidationError("password length must be greater than 3.")
    if len(password) > 100:
        raise ValidationError("password must not be greater than 100.")


# Autoschema maakt automatisch voor ieder column een field aan en voegt het toe aan de schema.
# je kan columns nog steeds zelf in schema neerzetten, dit wil je doen wanneer je extra validaties wilt toevoegen.
class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

    name = fields.Str(validate=validate.Length(min=2, max=30))
    email = fields.Str(validate=validate.Length(min=2, max=30))
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
