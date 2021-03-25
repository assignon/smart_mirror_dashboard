from models.user_model import User
from settings import ma

class UserSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = User
    

