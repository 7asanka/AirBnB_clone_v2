#!/usr/bin/python3
"""Unittest for State model"""
import unittest
import os
from models.state import State
from models.base_model import BaseModel


class TestState(unittest.TestCase):
    """Test class for State model"""

    def setUp(self):
        """Set up for each test method"""
        self.state = State()

    def tearDown(self):
        """Clean up after each test method"""
        del self.state

    def test_inheritance(self):
        """Test that State inherits from BaseModel"""
        self.assertIsInstance(self.state, BaseModel)

    def test_attributes(self):
        """Test attributes of State"""
        self.assertTrue(hasattr(self.state, "name"))
        self.assertEqual(self.state.name, "")

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "Testing DBStorage only")
    def test_db_storage_columns(self):
        """Test State attributes for DBStorage"""
        self.assertEqual(self.state.__tablename__, 'states')
        self.assertTrue(hasattr(self.state, 'name'))
        self.assertTrue(hasattr(self.state, 'cities'))

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Testing FileStorage only")
    def test_file_storage_behavior(self):
        """Test FileStorage behavior for State"""
        self.assertIsInstance(self.state.name, str)

    def test_to_dict(self):
        """Test the to_dict method"""
        state_dict = self.state.to_dict()
        self.assertEqual(state_dict["__class__"], "State")
        self.assertIn("id", state_dict)
        self.assertIn("created_at", state_dict)
        self.assertIn("updated_at", state_dict)

    def test_save(self):
        """Test the save method"""
        old_updated_at = self.state.updated_at
        self.state.save()
        self.assertNotEqual(self.state.updated_at, old_updated_at)

    def test_str(self):
        """Test the __str__ method"""
        expected_str = "[State] ({}) {}".format(self.state.id,
                                                self.state.__dict__)
        self.assertEqual(str(self.state), expected_str)
