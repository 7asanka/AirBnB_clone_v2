#!/usr/bin/python3
"""Unittest for BaseModel"""
from models.base_model import BaseModel
import unittest
import datetime
from uuid import UUID
import json
import os
from models import storage


class TestBaseModel(unittest.TestCase):
    """Test class for BaseModel"""

    def setUp(self):
        """Set up for each test method"""
        self.model = BaseModel()

    def tearDown(self):
        """Clean up after each test method"""
        try:
            os.remove('file.json')
        except FileNotFoundError:
            pass
        del self.model

    def test_default(self):
        """Test default instantiation of BaseModel"""
        self.assertIsInstance(self.model, BaseModel)

    def test_id(self):
        """Test id is a string and unique"""
        self.assertIsInstance(self.model.id, str)
        self.assertTrue(UUID(self.model.id, version=4))

    def test_created_at(self):
        """Test created_at is a datetime object"""
        self.assertIsInstance(self.model.created_at, datetime.datetime)

    def test_updated_at(self):
        """Test updated_at is a datetime object and updates on save"""
        old_updated_at = self.model.updated_at
        self.model.save()
        self.assertNotEqual(self.model.updated_at, old_updated_at)

    def test_str(self):
        """Test string representation of BaseModel"""
        expected_str = "[BaseModel] ({}) {}".format(self.model.id,
                                                    self.model.__dict__)
        self.assertEqual(str(self.model), expected_str)

    def test_to_dict(self):
        """Test to_dict method"""
        model_dict = self.model.to_dict()
        self.assertEqual(model_dict["__class__"], "BaseModel")
        self.assertIn("id", model_dict)
        self.assertIn("created_at", model_dict)
        self.assertIn("updated_at", model_dict)

    def test_kwargs(self):
        """Test instantiation with kwargs"""
        model_dict = self.model.to_dict()
        new_model = BaseModel(**model_dict)
        self.assertFalse(new_model is self.model)
        self.assertEqual(new_model.to_dict(), model_dict)

    def test_kwargs_invalid(self):
        """Test instantiation with invalid kwargs"""
        with self.assertRaises(TypeError):
            BaseModel(**{1: 2})

    def test_save(self):
        """Test save method"""
        self.model.save()
        storage.reload()
        key = f"BaseModel.{self.model.id}"
        if isinstance(storage.all(), dict):  # FileStorage
            self.assertIn(key, storage.all())
        else:  # DBStorage
            self.assertIn(self.model, storage.all(BaseModel).values())

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'file',
                     "FileStorage only")
    def test_file_storage_behavior(self):
        """Test FileStorage specific behavior"""
        self.model.save()
        key = f"BaseModel.{self.model.id}"
        with open('file.json', 'r') as f:
            data = json.load(f)
            self.assertIn(key, data)

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db', "DBStorage only")
    def test_db_storage_behavior(self):
        """Test DBStorage specific behavior"""
        self.model.save()
        storage.reload()
        self.assertIn(self.model, storage.all(BaseModel).values())
