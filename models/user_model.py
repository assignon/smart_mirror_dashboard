from datetime import datetime
from settings import db, bcrypt, ma
from flask_bcrypt import generate_password_hash, check_password_hash
from sqlalchemy import Column, Integer, String, DateTime, ForeignKeyConstraint, ForeignKey, CheckConstraint, Boolean, exc
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.sql.expression import desc
from .base_model import BaseMixin


class User(db.Model):
    __tablename__ = 'User'

    user_id = Column(Integer, primary_key=True)
    name = Column(String(length=50), nullable=False)
    login = Column(String(length=30), unique=True, nullable=False)
    password = Column(String(length=30), nullable=False)
    is_admin = Column(Boolean, nullable=False)


    def __repr__(self):
        return self.name

    @staticmethod
    def create(name, login, password, is_admin):
        """
        This function inserts a new row into the table and returns the new user
        """
        
        user = User(name=name, login=login, password=bcrypt.generate_password_hash(password).decode('utf8'), is_admin=is_admin)
        db.session.add(user)
        db.session.commit()

        return user


    @staticmethod
    def get_all_users():
        users = db.session.query(User).all()
        if users: 
            return db.session.query(User).all()
        else: raise NoResultFound


    @staticmethod
    def get_user(user_id):
        user = db.session.query(User).filter_by(user_id=user_id).first()
        if user: 
            return user
        else: raise NoResultFound
    

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
                setattr(user, column, value) 

            db.session.commit()
            return user
        else: 
            raise NoResultFound
    
    def get_user(self):
        return jsonify(dict({'id': 1, 'name': 'Yanick', 'admin': True, 'token': 'wsdhj98743puihsadnv36'}))
    

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
    

