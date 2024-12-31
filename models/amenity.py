#!/usr/bin/python3
""" Amenity Module for HBNB project """
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base


class Amenity(BaseModel, Base):
    """ Amenity class to represent amenities available at places """
    __tablename__ = 'amenities'

    name = Column(String(128), nullable=False)

    # Relationship with Place (Many-to-Many)
    place_amenities = relationship("Place", secondary="place_amenity",
                                   back_populates="amenities")
