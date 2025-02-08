#!/usr/bin/python3
"""DBStorage module for managing database storage with SQLAlchemy"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv
from models.base_model import Base
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DBStorage:
    """Manages database storage for hbnb models"""
    __engine = None
    __session = None

    def __init__(self):
        """Initialize the database engine"""
        # Retrieve environment variables
        user = getenv('HBNB_MYSQL_USER')
        pwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST', 'localhost')
        db = getenv('HBNB_MYSQL_DB')
        env = getenv('HBNB_ENV')

        # Create engine
        self.__engine = create_engine(
            f'mysql+mysqldb://{user}:{pwd}@{host}/{db}',
            pool_pre_ping=True
        )

        # Drop all tables if environment is 'test'
        if env == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Query all objects of a specific class, or all objects if cls is None.
        Returns a dictionary in the format:
        key = <class-name>.<object-id>, value = object
        """
        obj_dict = {}
        if cls:
            objects = self.__session.query(cls).all()
        else:
            classes = [User, State, City, Amenity, Place, Review]
            objects = []
            for cls in classes:
                objects.extend(self.__session.query(cls).all())

        for obj in objects:
            key = f"{type(obj).__name__}.{obj.id}"
            obj_dict[key] = obj
        return obj_dict

    def new(self, obj):
        """Add the object to the current database session"""
        if obj:
            self.__session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Delete obj from the current database session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Create all tables and initialize the current database session"""
        from sqlalchemy.orm import sessionmaker
        from sqlalchemy.orm import scoped_session

        Base.metadata.create_all(self.__engine)  # Create tables

        # Create a new session
        session_factory = sessionmaker(
            bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)

    def close(self):
	"""call remove() method on the
	private session attribute (self.__session)
	"""
	self.__session.remove()
