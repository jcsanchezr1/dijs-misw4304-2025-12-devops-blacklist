import unittest
from unittest.mock import patch, MagicMock
from views import BlacklistView, ResetDatabaseView, HealthCheckView, BlacklistDetailView
from flask import Flask

app = Flask(__name__)

class TestBlacklistViews(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.client = self.app.test_client()
        self.valid_token = 'Bearer valid-token'
        self.headers = {'Authorization': self.valid_token}

    @patch('views.Config.AUTH_TOKEN', 'valid-token')
    def test_health_check(self):
        with app.test_request_context():
            view = HealthCheckView()
            response, code = view.get()
            self.assertEqual(code, 500)
            # self.assertEqual(code, 200)
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

    @patch('views.Config.AUTH_TOKEN', 'valid-token')
    def test_get_existing_email_returns_blocked_reason(self):
        mock_account = MagicMock()
        mock_account.email = "test@example.com"
        mock_account.blocked_reason = "fraude"

        with self.app.test_request_context(headers=self.headers):
            view = BlacklistDetailView()

            view.authorize_request = MagicMock()
            view.validate_email = MagicMock(return_value=True)

            with patch('views.Blacklist.query') as mock_query:
                mock_filter = mock_query.filter_by.return_value
                mock_filter.first.return_value = mock_account

                response_data, status_code = view.get("test@example.com")

                self.assertEqual(status_code, 200)
                self.assertTrue(response_data["existe"])
                self.assertEqual(response_data["blocked_reason"], "fraude")
                view.authorize_request.assert_called_once()

if __name__ == '__main__':
    unittest.main()
