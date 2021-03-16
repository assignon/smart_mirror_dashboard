from datetime import datetime
from settings import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKeyConstraint, ForeignKey, CheckConstraint, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import desc
from sqlalchemy import exc

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
        return appointment

    @staticmethod
    def update_appointment(appointment_id, **kwargs):
        """
        This function updates the user in the database and returns the updated user.
        Input:
            user_id: id of the user that needs to be updated
            **kwargs: key value pairs, keys used should be the same as the columns specified in the model 
        """
        
        appointment = get_appointment(appointment_id)

        for column, value in kwargs.items():  
            setattr(appointment, column, value) 

        db.session.commit()
        return appointment