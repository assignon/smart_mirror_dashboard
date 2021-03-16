from datetime import datetime
from settings import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKeyConstraint, ForeignKey, CheckConstraint, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import desc
from sqlalchemy import exc
from .base_model import BaseMixin
from .appointment_model import Appointment
from .image_model import Image

class Guest(BaseMixin, db.Model):
    __tablename__ = 'Guest'

    guest_id = Column(Integer, primary_key=True)
    name = Column(String(length=50), nullable=False)
    email = Column(String(length=50), unique=True, nullable=False)
    company = Column(String(length=30))
    phone_number = Column(String(length=15), unique=True, nullable=False)
    license_plate = Column(String(length=30), unique=True)
    consent_duration = Column(Integer, nullable=False)
    appointments = relationship( "Appointment", order_by= "desc(Appointment.appointment_id)",lazy='joined', back_populates="guest")
    images = relationship("Image", order_by="desc(Image.image_id)", back_populates="guest")
    

    def __repr__(self):
        return f'Hallo ik ben {self.name}'


    def add_appointment(self, employee_name):
        """
        add an new appointment in the database
        Input: employee_name
        """
        Appointment.create(employee_name=employee_name, guest_id = self.guest_id)


    def add_images(self, filepath_images):
        """
        Hie komt functie om 1 of meedere afbeeldingen toe tevoegen aan guest
        """

        new_images = [Image(filepath=filepath_image, guest_id=self.guest_id) for filepath_image in filepath_images]
        db.session.add_all(new_images)
        db.session.commit()
    

    def get_images(self):
        
        images = db.session.query(Image).filter_by(guest_id=self.guest_id).all()
        
        return images
    

    @staticmethod
    def update_guest(guest_id, **kwargs):
        """
        This function updates the guest in the database and returns the updated guest.
        Input:
            guest_id: id of the guest that needs to be updated
            **kwargs: key value pairs, keys used should be the same as the columns specified in the model 
        """
        guest = db.session.query(Guest).filter_by(guest_id=guest_id).first()
        # terugkerende klant heeft afspraak met dezelfde employee
        if 'employee_name' not in kwargs.keys():
            most_recent_employee = guest.appointments[0].employee_name
            Appointment.create(employee_name=most_recent_employee, guest_id=guest_id)

        for column, value in kwargs.items():  
            # klant heeft afspraak met ander employee
            if column == 'employee_name':
                Appointment.create(employee_name=value, guest_id=guest_id)
            else:
                setattr(guest, column, value) 

            db.session.commit()
        return guest
        

    @staticmethod
    def get_guest(guest_id):
        """
        This function returns a guest object based on the guest_id
        """
        guest = db.session.query(Guest).filter_by(guest_id=guest_id).first()     
        
        return guest