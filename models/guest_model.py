# from settings import db, redis_db
from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound
# from .base_model import BaseMixin
# from .appointment_model import Appointment
from datetime import datetime
from sqlalchemy.sql import func


import os
import sys
try:
    sys.path.append(os.path.dirname(
        os.path.dirname(os.path.abspath(__file__))))
    # from .base_model import BaseMixin
    from settings import db, manager, redis_db
    from .appointment_model import Appointment
except:
    pass


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


class Guest(BaseMixin, db.Model):
    __tablename__ = 'Guest'

    guest_id = Column(Integer, primary_key=True)
    name = Column(String(length=50), nullable=False)
    email = Column(String(length=50), unique=True, nullable=False)
    company = Column(String(length=30))
    phone_number = Column(String(length=15), unique=True, nullable=False)
    license_plate = Column(String(length=30), unique=True)
    consent_expire_date = Column(Integer)
    appointments = relationship("Appointment", order_by="desc(Appointment.appointment_id)", lazy='joined',
                                back_populates="guest")

    def __repr__(self):
        return f'Hallo ik ben {self.name}'

    def add_appointment(self, employee_name):
        """
        add an new appointment in the database
        Input: employee_name
        """
        Appointment.create(employee_name=employee_name, guest_id=self.guest_id)

    @staticmethod
    def update_guest(guest_id, **kwargs):
        """
        This function updates the guest in the database and returns the updated guest.
        Input:
            guest_id: id of the guest that needs to be updated
            **kwargs: key value pairs, keys used should be the same as the columns specified in the model 
        """
        guest = db.session.query(Guest).filter_by(guest_id=guest_id).first()

        if guest:
            for column, value in kwargs.items():
                setattr(guest, column, value)

            db.session.commit()
            return guest
        else:
            raise NoResultFound

    @staticmethod
    def get_guest(guest_id):
        """
        This function returns a guest object based on the guest_id
        """

        guest = db.session.query(Guest).filter_by(guest_id=guest_id).first()
        if guest:
            return guest
        else:
            raise NoResultFound

    @staticmethod
    def delete_guest(guest_id):
        db.session.query(Guest).filter_by(guest_id=guest_id).delete()
        db.session.commit()
        redis_db.del_guest(guest_id)


if __name__ == '__main__':
    manager.run()
