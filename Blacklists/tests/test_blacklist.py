import unittest
from unittest.mock import patch, MagicMock
from views import BlacklistView, ResetDatabaseView, HealthCheckView
from flask import Flask

app = Flask(__name__)

class TestBlacklistViews(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()
        self.valid_token = 'Bearer valid-token'
        self.headers = {'Authorization': self.valid_token}

    @patch('views.Config.AUTH_TOKEN', 'valid-token')
    def test_health_check(self):
        with app.test_request_context():
            view = HealthCheckView()
            response, code = view.get()
            self.assertEqual(code, 200)
            self.assertEqual(response, 'pong')

    @patch('views.Config.AUTH_TOKEN', 'valid-token')
    @patch('views.db.session')
    def test_reset_database_success(self, mock_session):
        with app.test_request_context():
            view = ResetDatabaseView()
            response, code = view.post()
            self.assertEqual(code, 200)
            self.assertIn("Todos los datos fueron eliminados", response["msg"])
            mock_session.query.assert_called_once()
            mock_session.commit.assert_called_once()

    @patch('views.Config.AUTH_TOKEN', 'valid-token')
    def test_post_blacklist_success(self):
        with app.test_request_context(json={
            "email": "test@example.com",
            "app_uuid": "1234",
            "blocked_reason": "spam"
        }, headers=self.headers, environ_base={'REMOTE_ADDR': '127.0.0.1'}):
            
            view = BlacklistView()
            view.validate_email = MagicMock(return_value=True)
            view.account_exists = MagicMock(return_value=False)

            with patch('views.db.session.add'), patch('views.db.session.commit'):
                response, code = view.post()
                self.assertEqual(code, 201)
                self.assertIn("msg", response)

    @patch('views.Config.AUTH_TOKEN', 'valid-token')
    def test_post_blacklist_invalid_email(self):
        with app.test_request_context(json={
            "email": "invalid",
            "app_uuid": "1234",
            "blocked_reason": "spam"
        }, headers=self.headers):
            
            view = BlacklistView()
            view.validate_email = MagicMock(return_value=False)

            with self.assertRaises(Exception) as context:
                view.post()      


if __name__ == '__main__':
    unittest.main()
