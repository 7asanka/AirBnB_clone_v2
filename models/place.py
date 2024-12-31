#!/usr/bin/python3
""" Place Module for HBNB project """
from sqlalchemy import Table, Column, String, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship
from models.base_model import BaseModel, Base
import models
from os import getenv


# Association Table for Many-to-Many relationship between Place and Amenity
place_amenity = Table(
    'place_amenity',
    Base.metadata,
    Column('place_id', String(60), ForeignKey('places.id'),
           primary_key=True, nullable=False),
    Column('amenity_id', String(60), ForeignKey('amenities.id'),
           primary_key=True, nullable=False)
)


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'

    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024), nullable=True)
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    amenities = relationship("Amenity", secondary="place_amenity",
                             back_populates="place_amenities", viewonly=False)

    if getenv('HBNB_TYPE_STORAGE') != 'db':
        @property
        def amenities(self):
            """Getter for amenities in FileStorage"""
            return [amenity for amenity
                    in models.storage.all('Amenity').values()
                    if amenity.id in self.amenity_ids]

        @amenities.setter
        def amenities(self, obj):
            """Setter for amenities in FileStorage"""
            if isinstance(obj, models.Amenity):
                if obj.id not in self.amenity_ids:
                    self.amenity_ids.append(obj.id)

    amenity_ids = []
