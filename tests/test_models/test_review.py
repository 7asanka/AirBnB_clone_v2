#!/usr/bin/python3
"""Unittest for Review model"""
import unittest
import os
from models.review import Review
from models.base_model import BaseModel


class TestReview(unittest.TestCase):
    """Test class for Review model"""

    def setUp(self):
        """Set up for each test method"""
        self.review = Review()

    def tearDown(self):
        """Clean up after each test method"""
        del self.review

    def test_inheritance(self):
        """Test that Review inherits from BaseModel"""
        self.assertIsInstance(self.review, BaseModel)

    def test_attributes(self):
        """Test attributes of Review"""
        self.assertTrue(hasattr(self.review, "place_id"))
        self.assertTrue(hasattr(self.review, "user_id"))
        self.assertTrue(hasattr(self.review, "text"))

        self.assertEqual(self.review.place_id, "")
        self.assertEqual(self.review.user_id, "")
        self.assertEqual(self.review.text, "")

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') != 'db',
                     "Testing DBStorage only")
    def test_db_storage_columns(self):
        """Test Review attributes for DBStorage"""
        self.assertEqual(self.review.__tablename__, 'reviews')
        self.assertTrue(hasattr(self.review, 'place_id'))
        self.assertTrue(hasattr(self.review, 'user_id'))
        self.assertTrue(hasattr(self.review, 'text'))

    @unittest.skipIf(os.getenv('HBNB_TYPE_STORAGE') == 'db',
                     "Testing FileStorage only")
    def test_file_storage_behavior(self):
        """Test FileStorage behavior for Review"""
        self.assertIsInstance(self.review.place_id, str)
        self.assertIsInstance(self.review.user_id, str)
        self.assertIsInstance(self.review.text, str)

    def test_to_dict(self):
        """Test the to_dict method"""
        review_dict = self.review.to_dict()
        self.assertEqual(review_dict["__class__"], "Review")
        self.assertIn("id", review_dict)
        self.assertIn("created_at", review_dict)
        self.assertIn("updated_at", review_dict)

    def test_save(self):
        """Test the save method"""
        old_updated_at = self.review.updated_at
        self.review.save()
        self.assertNotEqual(self.review.updated_at, old_updated_at)

    def test_str(self):
        """Test the __str__ method"""
        expected_str = "[Review] ({}) {}".format(self.review.id,
                                                 self.review.__dict__)
        self.assertEqual(str(self.review), expected_str)
