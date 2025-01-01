#!/usr/bin/python3
"""Unittest for City model"""
import unittest
import os
from models.city import City
from models.base_model import BaseModel


class TestCity(unittest.TestCase):
    """Test class for City model"""

    def setUp(self):
        """Set up for each test method"""
        self.city = City()

    def tearDown(self):
        """Clean up after each test method"""
        del self.city

    def test_inheritance(self):
        """Test that City inherits from BaseModel"""
        self.assertIsInstance(self.city, BaseModel)

    def test_attributes(self):
        """Test attributes of City"""
        self.assertTrue(hasattr(self.city, "state_id"))
        self.assertTrue(hasattr(self.city, "name"))
        self.assertEqual(self.city.state_id, "")
        self.assertEqual(self.city.name, "")

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "Testing DBStorage only")
    def test_db_storage_columns(self):
        """Test City attributes for DBStorage"""
        self.assertEqual(self.city.__tablename__, 'cities')
        self.assertTrue(hasattr(self.city, 'state_id'))
        self.assertTrue(hasattr(self.city, 'name'))

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Testing FileStorage only")
    def test_file_storage_behavior(self):
        """Test FileStorage behavior for City"""
        self.assertTrue(isinstance(self.city.state_id, str))
        self.assertTrue(isinstance(self.city.name, str))

    def test_to_dict(self):
        """Test the to_dict method"""
        city_dict = self.city.to_dict()
        self.assertEqual(city_dict["__class__"], "City")
        self.assertIn("id", city_dict)
        self.assertIn("created_at", city_dict)
        self.assertIn("updated_at", city_dict)

    def test_save(self):
        """Test the save method"""
        old_updated_at = self.city.updated_at
        self.city.save()
        self.assertNotEqual(self.city.updated_at, old_updated_at)

    def test_str(self):
        """Test the __str__ method"""
        expected_str = "[City] ({}) {}".format(self.city.id,
                                               self.city.__dict__)
        self.assertEqual(str(self.city), expected_str)
