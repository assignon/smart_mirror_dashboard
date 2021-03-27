from datetime import datetime
from settings import db, bcrypt, ma
from flask_bcrypt import generate_password_hash, check_password_hash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, create_refresh_token
from sqlalchemy import Column, Integer, String, DateTime, ForeignKeyConstraint, ForeignKey, CheckConstraint, Boolean, exc
from sqlalchemy.orm import relationship
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
        This function inserts a new row into the table and returns a tuple (boolean succes, obj)
        obj contains instance of the class if succes = True, if False it contains the error message.
        arguments should match the column names specified in the model
        """
        
        succes = True
        user = User(name=name, login=login, password=bcrypt.generate_password_hash(password).decode('utf8'), is_admin=is_admin)
        db.session.add(user)
        try:
            db.session.commit()
        except exc.IntegrityError as e:
            db.session.rollback()
            succes = False
            user = e.orig.args 


        return succes, user


    @staticmethod
    def get_all_users():
        return db.session.query(User).all()


    @staticmethod
    def get_user(user_id):
        user = db.session.query(User).filter_by(user_id=user_id).first()
        return user
    

    @staticmethod
    def update_user(user_id, **kwargs):
        """
        This function updates the user in the database and returns the updated user.
        Input:
            user_id: id of the user that needs to be updated
            **kwargs: key value pairs, keys used should be the same as the columns specified in the model 
        """
        
        user = User.get_user(user_id)

        for column, value in kwargs.items():  
            setattr(user, column, value) 

        db.session.commit()
        return user
    

    @staticmethod
    def delete_user(user_id):
        User.query.filter_by(user_id=user_id).delete()
        db.session.commit()


    def check_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
    

