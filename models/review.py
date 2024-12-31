#!/usr/bin/python3
""" Review module for the HBNB project """
from sqlalchemy import Column, String, ForeignKey
from models.base_model import BaseModel


class Review(BaseModel):
    """ Review classto store review information """
    __tabelname__ = 'reviews'

    text = Column(String(1024), nullable=False)
    place_id = Column(String(60), ForeignKey('places.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
