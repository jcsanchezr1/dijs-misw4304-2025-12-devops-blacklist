import os
os.environ['TESTING'] = '1'

import unittest
from unittest.mock import patch, MagicMock
from config import Config
from app import app
class TestBlacklistViews(unittest.TestCase):

    def setUp(self):
        app.config['TESTING'] = True
        self.client = app.test_client()
        self.app = app
        self.valid_token = 'Bearer valid-token'
        self.headers = {'Authorization': self.valid_token}

        self.endpoint_blacklists = "/blacklists/email@mail.com"
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch('views.Config.AUTH_TOKEN', 'valid-token')
    def test_health_check(self):
        with self.app.test_request_context():
            from views import HealthCheckView
            view = HealthCheckView()
            response, code = view.get()
            self.assertEqual(code, 200)
            self.assertEqual(response, 'pong')

    @patch('views.Config.AUTH_TOKEN', 'valid-token')
    @patch('views.db.session')
    def test_reset_database_success(self, mock_session):
        with self.app.test_request_context():
            from views import ResetDatabaseView
            view = ResetDatabaseView()
            response, code = view.post()
            self.assertEqual(code, 200)
            self.assertIn("Todos los datos fueron eliminados", response["msg"])
            mock_session.query.assert_called_once()
            mock_session.commit.assert_called_once()

    @patch('views.Config.AUTH_TOKEN', 'valid-token')
    def test_post_blacklist_success(self):
        with self.app.test_request_context(json={
            "email": "test@example.com",
            "app_uuid": "1234",
            "blocked_reason": "spam"
        }, headers=self.headers, environ_base={'REMOTE_ADDR': '127.0.0.1'}):
            from views import BlacklistView
            view = BlacklistView()
            view.validate_email = MagicMock(return_value=True)
            view.account_exists = MagicMock(return_value=False)

            with patch('views.db.session.add'), patch('views.db.session.commit'):
                response, code = view.post()
                self.assertEqual(code, 201)
                self.assertIn("msg", response)

    @patch('views.Config.AUTH_TOKEN', 'valid-token')    
    def test_post_blacklist_invalid_email(self):
        with self.app.test_request_context(json={
            "email": "invalid",
            "app_uuid": "1234",
            "blocked_reason": "spam"
        }, headers=self.headers):
            from views import BlacklistView
            view = BlacklistView()
            view.validate_email = MagicMock(return_value=False)

            with self.assertRaises(Exception):
                view.post()

    @patch.object(Config, 'AUTH_TOKEN', 'valid_token')
    @patch('models.Blacklist.query')
    def test_get_blacklist_with_email(self, mock_query):
        email = "email@mail.com"

        mock_query.filter_by.return_value.first.return_value = None

        response = self.client.get(
            f"/blacklists/{email}",
            headers={"Authorization": "Bearer valid_token"},
        )

        self.assertEqual(response.status_code, 200)
        response_data = response.get_json()
        self.assertEqual(response_data['existe'], False)
        self.assertEqual(response_data['blocked_reason'], '')



if __name__ == '__main__':
    unittest.main()
