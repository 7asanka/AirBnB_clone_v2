#!/usr/bin/python3
"""This module instantiates a storage object based on the storage type"""

from os import getenv

storage_t = getenv('HBNB_TYPE_STORAGE', 'file')

if storage_t == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()
else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
