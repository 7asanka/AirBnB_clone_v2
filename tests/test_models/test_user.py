#!/usr/bin/python3
"""Unittest for User model"""
import unittest
import os
from models.user import User
from models.base_model import BaseModel


class TestUser(unittest.TestCase):
    """Test class for User model"""

    def setUp(self):
        """Set up for each test method"""
        self.user = User()

    def tearDown(self):
        """Clean up after each test method"""
        del self.user

    def test_inheritance(self):
        """Test that User inherits from BaseModel"""
        self.assertIsInstance(self.user, BaseModel)

    def test_attributes(self):
        """Test attributes of User"""
        self.assertTrue(hasattr(self.user, "email"))
        self.assertTrue(hasattr(self.user, "password"))
        self.assertTrue(hasattr(self.user, "first_name"))
        self.assertTrue(hasattr(self.user, "last_name"))

        self.assertEqual(self.user.email, "")
        self.assertEqual(self.user.password, "")
        self.assertEqual(self.user.first_name, "")
        self.assertEqual(self.user.last_name, "")

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "Testing DBStorage only")
    def test_db_storage_columns(self):
        """Test User attributes for DBStorage"""
        self.assertEqual(self.user.__tablename__, 'users')
        self.assertTrue(hasattr(self.user, 'places'))
        self.assertTrue(hasattr(self.user, 'reviews'))

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Testing FileStorage only")
    def test_file_storage_behavior(self):
        """Test FileStorage behavior for User"""
        self.assertIsInstance(self.user.email, str)
        self.assertIsInstance(self.user.password, str)
        self.assertIsInstance(self.user.first_name, str)
        self.assertIsInstance(self.user.last_name, str)

    def test_to_dict(self):
        """Test the to_dict method"""
        user_dict = self.user.to_dict()
        self.assertEqual(user_dict["__class__"], "User")
        self.assertIn("id", user_dict)
        self.assertIn("created_at", user_dict)
        self.assertIn("updated_at", user_dict)

    def test_save(self):
        """Test the save method"""
        old_updated_at = self.user.updated_at
        self.user.save()
        self.assertNotEqual(self.user.updated_at, old_updated_at)

    def test_str(self):
        """Test the __str__ method"""
        expected_str = "[User] ({}) {}".format(self.user.id,
                                               self.user.__dict__)
        self.assertEqual(str(self.user), expected_str)
