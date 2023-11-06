import unittest
from qnap_exporter.app import create_app
from qnap_exporter.app.config import test_config


class TestRoutes(unittest.TestCase):
    def setUp(self):
        app = create_app(test_config)
        self.app = app.test_client()

    def test_hey(self):
        resp = self.app.get('/hey', follow_redirects=True)
        self.assertEqual(resp.json, {'message': 'in a bottle'})


if __name__ == '__main__':
    unittest.main()
