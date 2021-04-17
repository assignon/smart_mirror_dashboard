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
        This function inserts a new row into the table and returns the row that has been added.
        """

        obj = cls(**kw)
        db.session.add(obj)
        db.session.commit()

        return obj
