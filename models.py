from sqlalchemy import Column, Integer, String, DateTime, ForeignKeyConstraint, ForeignKey, CheckConstraint, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import desc
from sqlalchemy import exc
import os
import sys



currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)
# settings import should be under the code on line 7 to 9
from settings import DataBase as db


class BaseMixin(object):
    @classmethod
    def create(cls, **kw):
        """
        This function inserts a new row into the table and returns a tuple (boolean succes, obj)
        obj contains guest instance if succus = True, if False it contains the error message.
        arguments should match the column names specified in the model
        """
        with db() as dbase:
            succes = True
            obj = cls(**kw)
            dbase.session.add(obj)
            try:
                dbase.session.commit()
            except exc.IntegrityError as e:
                dbase.session.rollback()
                succes = False
                obj = e.orig.args 


        return succes, obj
        

class User(BaseMixin, db.Base):
    __tablename__ = 'User'

    user_id = Column(Integer, primary_key=True)
    name = Column(String(length=50), nullable=False)
    login = Column(String(length=30), unique=True, nullable=False)
    password = Column(String(length=30), nullable=False)
    is_admin = Column(Boolean, nullable=False)

    @staticmethod
    def update_user(user_id, **kwargs):
        """
        This function updates the user in the database and returns the updated user.
        Input:
            user_id: id of the user that needs to be updated
            **kwargs: key value pairs, keys used should be the same as the columns specified in the model 
        """
        with db() as dbase:
            user = dbase.session.query(User).filter_by(user_id=user_id).first()

            for column, value in kwargs.items():  
                setattr(user, column, value) 

            dbase.session.commit()
        return user



class Guest(BaseMixin, db.Base):
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
        with db() as dbase:
            new_images = [Image(filepath=filepath_image, guest_id=self.guest_id) for filepath_image in filepath_images]
            dbase.session.add_all(new_images)
            dbase.session.commit()
    

    def get_images(self):
        with db() as dbase:
            images = dbase.session.query(Image).filter_by(guest_id=self.guest_id).all()
        
        return images
    

    @staticmethod
    def update_guest(guest_id, **kwargs):
        """
        This function updates the guest in the database and returns the updated guest.
        Input:
            guest_id: id of the guest that needs to be updated
            **kwargs: key value pairs, keys used should be the same as the columns specified in the model 
        """
        with db() as dbase:
            guest = dbase.session.query(Guest).filter_by(guest_id=guest_id).first()
            # terugkerende klant heeft afspraak met dezelfde employee
            if 'employee_name' not in kwargs.keys():
                most_recent_employee = guest.appointments[0].employee_name
                Appointment.create(employee_name=most_recent_employee, guest_id=guest_id)

            for column, value in kwargs.items():  
                # klant heeft afspraak met ander employee
                if column == 'employee_name':
                    Appointment.create(employee_name=value, guest_id=guest_id)

                setattr(guest, column, value) 

            dbase.session.commit()
        return guest
        

    @staticmethod
    def get_guest(guest_id):
        """
        This function returns a guest object based on the guest_id
        """
        with db() as dbase:
            guest = dbase.session.query(Guest).filter_by(guest_id=guest_id).first()     
        
        return guest
    

class Appointment(BaseMixin, db.Base):
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
 


class Image(BaseMixin, db.Base):
    __tablename__ = 'Image'
    image_id = Column(Integer, primary_key=True)
    filepath = Column(String)
    # nieuwe column
    date = Column(DateTime)
    guest_id = Column(Integer, ForeignKey(
        'Guest.guest_id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    guest = relationship("Guest", back_populates="images")


    @staticmethod
    def add_images(filepath_images, guest_id):
        """
        Add new labeled images to the database
        """
        with db() as dbase:
            new_images = [Image(filepath=filepath_image, guest_id=guest_id) for filepath_image in filepath_images]
            dbase.session.add_all(new_images)
            dbase.session.commit()
    
    @staticmethod
    def get_images(guest_id=False):
        """get all labeled images from the image table, returns images of guest if specified"""
        with db() as dbase:
            if guest_id:
                images = dbase.session.query(Image).filter_by(guest_id=guest_id).all()
            else:
                images = dbase.session.query(Image).all()
        return images
    

    @staticmethod
    def update_image(image_id, **kwargs):
        """
        This function updates the image in the database and returns the updated image.
        Input:
            image_id: id of the image that needs to be updated
            **kwargs: key value pairs, keys used should be the same as the columns specified in the model 
        """
        with db() as dbase:
            image = dbase.session.query(Image).filter_by(image_id=image_id).first()

            for column, value in kwargs.items():  
                setattr(image, column, value) 

            dbase.session.commit()
        return image
    
    
def create_db():
    # create all DB tables of this model file
    db.Base.metadata.create_all(db.engine)