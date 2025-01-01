#!/usr/bin/python3
"""Unittest for FileStorage"""
import unittest
import os
from models.base_model import BaseModel
from models import storage
from models.engine.file_storage import FileStorage


class TestFileStorage(unittest.TestCase):
    """Test class for FileStorage"""

    def setUp(self):
        """Set up test environment"""
        self.file_path = FileStorage._FileStorage__file_path
        self.objects = FileStorage._FileStorage__objects
        # Clear objects dictionary
        self.objects.clear()

    def tearDown(self):
        """Clean up after each test method"""
        try:
            os.remove(self.file_path)
        except FileNotFoundError:
            pass

    def test_all_returns_dict(self):
        """Test that all() returns the __objects dictionary"""
        self.assertIsInstance(storage.all(), dict)

    def test_new(self):
        """Test that new() adds an object to __objects"""
        obj = BaseModel()
        key = f"BaseModel.{obj.id}"
        self.assertIn(key, storage.all())
        self.assertEqual(storage.all()[key], obj)

    def test_save_creates_file(self):
        """Test that save() creates a file"""
        obj = BaseModel()
        storage.save()
        self.assertTrue(os.path.exists(self.file_path))

    def test_save_content(self):
        """Test that save() writes content to the file"""
        obj = BaseModel()
        storage.save()
        with open(self.file_path, 'r') as f:
            content = f.read()
        self.assertIn(f"BaseModel.{obj.id}", content)

    def test_reload(self):
        """Test that reload() loads objects from the file"""
        obj = BaseModel()
        storage.save()
        storage.reload()
        key = f"BaseModel.{obj.id}"
        self.assertIn(key, storage.all())
        self.assertEqual(storage.all()[key].id, obj.id)

    def test_reload_empty_file(self):
        """Test that reload() raises no error for an empty file"""
        with open(self.file_path, 'w'):
            pass
        try:
            storage.reload()
        except Exception as e:
            self.fail(f"reload() raised {type(e).__name__} unexpectedly!")

    def test_reload_no_file(self):
        """Test that reload() does nothing if the file does not exist"""
        try:
            os.remove(self.file_path)
        except FileNotFoundError:
            pass
        self.assertIsNone(storage.reload())

    def test_save_and_reload(self):
        """Test save() and reload() together"""
        obj = BaseModel()
        obj.save()
        storage.reload()
        key = f"BaseModel.{obj.id}"
        self.assertIn(key, storage.all())

    def test_key_format(self):
        """Test that keys in __objects are properly formatted"""
        obj = BaseModel()
        key = f"BaseModel.{obj.id}"
        self.assertIn(key, storage.all())

    def test_storage_variable_created(self):
        """Test that storage is an instance of FileStorage"""
        self.assertIsInstance(storage, FileStorage)

    def test_file_path_is_string(self):
        """Test that __file_path is a string"""
        self.assertIsInstance(self.file_path, str)

    def test_objects_is_dict(self):
        """Test that __objects is a dictionary"""
        self.assertIsInstance(storage.all(), dict)

    def test_save_updates_file(self):
        """Test that save() updates the file content"""
        obj = BaseModel()
        storage.save()
        with open(self.file_path, 'r') as f:
            content = f.read()
        self.assertIn(obj.id, content)

    def test_reload_missing_file(self):
        """Test that reload() does nothing if the file is missing"""
        try:
            os.remove(self.file_path)
        except FileNotFoundError:
            pass
        self.assertIsNone(storage.reload())
