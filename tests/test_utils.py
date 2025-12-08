"""
Unit tests for utils module
"""

import unittest
from datetime import datetime
from utils import (
    format_date,
    calculate_days_remaining,
    validate_grade,
    get_priority_level
)


class TestUtils(unittest.TestCase):
    def test_format_date_valid(self):
        """Test format_date with valid date string"""
        result = format_date("2024-12-25")
        self.assertIsInstance(result, datetime)
        self.assertEqual(result.year, 2024)
        self.assertEqual(result.month, 12)
        self.assertEqual(result.day, 25)

    def test_validate_grade_valid(self):
        """Test validate_grade with valid grades"""
        self.assertTrue(validate_grade(85))
        self.assertTrue(validate_grade(0))
        self.assertTrue(validate_grade(100))
        self.assertTrue(validate_grade(50.5))

    def test_validate_grade_invalid(self):
        """Test validate_grade with invalid grades"""
        self.assertFalse(validate_grade(-1))
        self.assertFalse(validate_grade(101))
        self.assertFalse(validate_grade(150))

    def test_get_priority_level(self):
        """Test priority level calculation"""
        self.assertEqual(get_priority_level(-1), "OVERDUE")
        self.assertEqual(get_priority_level(2), "HIGH")
        self.assertEqual(get_priority_level(5), "MEDIUM")
        self.assertEqual(get_priority_level(10), "LOW")


if __name__ == '__main__':
    unittest.main()