from datetime import datetime
from settings import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKeyConstraint, ForeignKey, CheckConstraint, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import desc
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import exc
from .base_model import BaseMixin

class Appointment(BaseMixin, db.Model):
    __tablename__ = 'Appointment'

    appointment_id = Column(Integer, primary_key=True)
    checked_in = Column(DateTime)
    checked_out = Column(DateTime)
    #pass id = NULL means guest doesnt have a pass
    pass_id = Column(Integer)
    employee_name = Column(String(length=50))
    guest_id = Column(Integer, ForeignKey('Guest.guest_id',
                                          onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    guest = relationship("Guest", back_populates="appointments", lazy='joined')


    @staticmethod
    def get_appointment(appointment_id):
        appointment = db.session.query(Appointment).filter(appointment_id=appointment_id).first()
        if appointment:
            return appointment
        else: 
            raise NoResultFound


    @staticmethod
    def update_appointment(appointment_id, **kwargs):
        """
        This function updates the appointment in the database and returns the updated appointment.
        Input:
            appoinment_id: id of the appointment that needs to be updated
            **kwargs: key value pairs, keys used should be the same as the columns specified in the model 
        """
        
        appointment = Appointment.query.filter_by(appointment_id=appointment_id).first()

        if appointment:

            for column, value in kwargs.items():  
                setattr(appointment, column, value) 

            db.session.commit()
            return appointment
        
        else:
            raise NoResultFound



    @staticmethod
    def delete_appointment(appointment_id):
        db.session.query(Appointment).filter_by(appointment_id=appointment_id).delete()
        db.session.commit()
