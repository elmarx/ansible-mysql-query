import unittest

from library.mysql_query import weak_equals


class WeakEquals(unittest.TestCase):

    def test_int_int(self):
        self.assertTrue(weak_equals(42, 42))
        self.assertFalse(weak_equals(42, 43))

    def test_string_string(self):
        self.assertTrue(weak_equals("a", "a"))
        self.assertFalse(weak_equals("a", "b"))

    def test_string_int(self):
        self.assertTrue(weak_equals("1", 1))
        self.assertTrue(weak_equals(1, "1"))
        self.assertFalse(weak_equals("2", 1))
        self.assertFalse(weak_equals(1, "2"))

    def test_string_long(self):
        self.assertTrue(weak_equals("1", 1L))
        self.assertTrue(weak_equals(1L, "1"))
        self.assertFalse(weak_equals("2", 1L))
        self.assertFalse(weak_equals(1L, "2"))

    def test_string_float(self):
        self.assertTrue(weak_equals("1.1", 1.1))
        self.assertTrue(weak_equals(1.1, "1.1"))
        self.assertFalse(weak_equals("2", 1.1))
        self.assertFalse(weak_equals(1.1, "2"))


