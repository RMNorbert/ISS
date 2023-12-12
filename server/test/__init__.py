import unittest
from flask_testing import TestCase
from server.__main__ import app


class BaseTestCase(TestCase):
    def create_app(self):
        return app


if __name__ == '__main__':
    unittest.main()
