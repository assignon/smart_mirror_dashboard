from settings import db, bcrypt, ma
from sqlalchemy import Column, Integer, String,  Boolean
from sqlalchemy.orm.exc import NoResultFound



class User(db.Model):
    __tablename__ = 'User'

    user_id = Column(Integer, primary_key=True)
    name = Column(String(length=50), nullable=False)
    email = Column(String(length=30),nullable=False, unique=True)
    password = Column(String(length=30), nullable=False)
    is_admin = Column(Boolean, nullable=False)

    def __repr__(self):
        return self.name

    @staticmethod
    def create(name, email, password, is_admin):
        """
        This function inserts a new row into the table and returns the new user
        """

        user = User(name=name, email=email, password=bcrypt.generate_password_hash(password).decode('utf8'),
                    is_admin=is_admin)
        db.session.add(user)
        db.session.commit()

        return user

    @staticmethod
    def get_all_users():
        users = db.session.query(User).all()
        if users:
            return db.session.query(User).all()
        else:
            raise NoResultFound

    @staticmethod
    def get_user(user_id):
        user = db.session.query(User).filter_by(user_id=user_id).first()
        if user:
            return user
        else:
            raise NoResultFound

    @staticmethod
    def update_user(user_id, **kwargs):
        """
        This function updates the user in the database and returns the updated user.
        Input:
            user_id: id of the user that needs to be updated
            **kwargs: key value pairs, keys used should be the same as the columns specified in the model 
        """

        user = User.get_user(user_id)
        if user:
            for column, value in kwargs.items():
                if column == "password":
                    print('trying the new password')
                    value = bcrypt.generate_password_hash(value).decode('utf8')
                setattr(user, column, value)

            db.session.commit()
            return user
        else:
            raise NoResultFound

    # def get_user(self):
    #     return jsonify(dict({'id': 1, 'name': 'Yanick', 'admin': True, 'token': 'wsdhj98743puihsadnv36'}))

    @staticmethod
    def delete_user(user_id):
        User.query.filter_by(user_id=user_id).delete()
        db.session.commit()

    def check_password(self, password) -> bool:
        return bcrypt.check_password_hash(self.password, password)


class SocketUserManager(db.Model):
    """
    manage the connected and disconnected user to the socket

    Args:
        db (obj): [Db object]
    """
    _id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)

    def connected_user(self, user_id):
        """
        add connected user to the socket

        Args:
            user_id (int): [user id]
        """
        pass

    def disconnected_user(self, user_id):
        """
        remove disconnecte user fron the socket

        Args:
            user_id (int): [user id]
        """
        pass

    def get_connected_user(self):
        """
        get all connected user id
        """
        pass

    @staticmethod
    def delete_user(user_id):
        User.query.filter_by(user_id=user_id).delete()
        db.session.commit()

    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
