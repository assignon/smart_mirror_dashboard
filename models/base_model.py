from datetime import datetime
from settings import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKeyConstraint, ForeignKey, CheckConstraint, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import desc
from sqlalchemy import exc



class BaseMixin(object):
    @classmethod
    def create(cls, **kw):
        """
        This function inserts a new row into the table and returns a tuple (boolean succes, obj)
        obj contains instance of the class if succes = True, if False it contains the error message.
        arguments should match the column names specified in the model
        """
        
        succes = True
        obj = cls(**kw)
        db.session.add(obj)
        try:
            db.session.commit()
        except exc.IntegrityError as e:
            db.session.rollback()
            succes = False
            obj = e.orig.args 


        return succes, obj