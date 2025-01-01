#!/usr/bin/python3
"""Unittest for Amenity model"""
import unittest
import os
from models.amenity import Amenity
from models.base_model import BaseModel


class TestAmenity(unittest.TestCase):
    """Test class for Amenity model"""

    def setUp(self):
        """Set up for each test method"""
        self.amenity = Amenity()

    def tearDown(self):
        """Clean up after each test method"""
        del self.amenity

    def test_inheritance(self):
        """Test that Amenity inherits from BaseModel"""
        self.assertIsInstance(self.amenity, BaseModel)

    def test_attributes(self):
        """Test attributes of Amenity"""
        self.assertTrue(hasattr(self.amenity, "name"))
        self.assertEqual(self.amenity.name, "")

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "Testing DBStorage only")
    def test_db_storage_columns(self):
        """Test Amenity attributes for DBStorage"""
        self.assertEqual(self.amenity.__tablename__, 'amenities')
        self.assertTrue(hasattr(self.amenity, 'place_amenities'))

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Testing FileStorage only")
    def test_file_storage_behavior(self):
        """Test FileStorage behavior for Amenity"""
        self.assertTrue(isinstance(self.amenity.name, str))

    def test_to_dict(self):
        """Test the to_dict method"""
        amenity_dict = self.amenity.to_dict()
        self.assertEqual(amenity_dict["__class__"], "Amenity")
        self.assertIn("created_at", amenity_dict)
        self.assertIn("updated_at", amenity_dict)

    def test_save(self):
        """Test the save method"""
        old_updated_at = self.amenity.updated_at
        self.amenity.save()
        self.assertNotEqual(self.amenity.updated_at, old_updated_at)

    def test_str(self):
        """Test the __str__ method"""
        expected_str = "[Amenity] ({}) {}".format(self.amenity.id,
                                                  self.amenity.__dict__)
        self.assertEqual(str(self.amenity), expected_str)
