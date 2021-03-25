from models.user_model import User
from settings import ma
from marshmallow import validates, validate, ValidationError

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User

    @validates("login")
    def validate_quantity(self, value):
        if  len(value) < 3:
            raise ValidationError("length must be greater than 3.")
        if len(value) > 30:
            raise ValidationError("length must not be greater than 30.")
    


# from models.user_model import User
# from settings import ma
# from marshmallow import validates, validate

# class UserSchema(ma.SQLAlchemySchema):
#     class Meta:
#         model = User
    
#     user_id = ma.auto_field()
#     name = ma.auto_field(validate.Length(min=3))
#     login = ma.auto_field(validate.Length(min=3))
#     password = ma.auto_field(validate.Length(min=5))
#     is_admin = ma.auto_field()
    

