from datetime import datetime
from settings import db
from sqlalchemy import Column, Integer, String, DateTime, ForeignKeyConstraint, ForeignKey, CheckConstraint, Boolean, \
    Date
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import desc
from sqlalchemy.sql import func
from sqlalchemy import exc
from .base_model import BaseMixin


class Image(BaseMixin, db.Model):
    __tablename__ = 'Image'
    image_id = Column(Integer, primary_key=True)
    filepath = Column(String)
    # nieuwe column
    date = Column(Date, default=func.current_date())
    guest_id = Column(Integer, ForeignKey(
        'Guest.guest_id', onupdate="CASCADE", ondelete="CASCADE"), nullable=False)
    guest = relationship("Guest", back_populates="images")

    @staticmethod
    def add_images(filepath_images, guest_id):
        """
        Add new labeled images to the database
        """
        new_images = [Image(filepath=filepath_image, guest_id=guest_id) for filepath_image in filepath_images]
        db.session.add_all(new_images)
        db.session.commit()

    @staticmethod
    def get_images(guest_id=False):
        """get all labeled images from the image table, returns images of guest if specified"""
        if guest_id:
            images = db.session.query(Image).filter_by(guest_id=guest_id).all()
        else:
            images = db.session.query(Image).all()
        return images

    @staticmethod
    def update_image(image_id, **kwargs):
        """
        This function updates the image in the database and returns the updated image.
        Input:
            image_id: id of the image that needs to be updated
            **kwargs: key value pairs, keys used should be the same as the columns specified in the model 
        """
        image = db.session.query(Image).filter_by(image_id=image_id).first()

        for column, value in kwargs.items():
            setattr(image, column, value)

        db.session.commit()
        return image
