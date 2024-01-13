import unittest
from unit_tests_py.func import func_ok


class TestCases(unittest.TestCase):
    def test1(self):
        self.assertEqual(func_ok(2, 0), True)

    def test2(self):
        self.assertEqual(func_ok(1, 2), True)

    def test3(self):
        self.assertEqual(func_ok(0.5, 1.5), True)

    def test4(self):
        self.assertEqual(func_ok("g", 1.5), True)

    def test5(self):
        self.assertEqual(func_ok("g", 2), True)


if __name__ == "__main__":
    unittest.main()
