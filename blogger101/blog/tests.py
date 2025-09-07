from django.test import TestCase
from unittest.mock import patch, MagicMock
from rest_framework.test import APIClient


class UserAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    @patch("blog.views.User.objects")
    def test_create_user_success(self, mock_objects):
        # Mock objects.filter().exists() -> False
        mock_objects.filter.return_value.exists.return_value = False

        # Mock user instance
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.username = "test01"
        mock_user.email = "test01@example.com"
        mock_objects.create.return_value = mock_user

        data = {"username": "test01", "password": "test01", "email": "test01@example.com"}
        response = self.client.post("/api/user", data, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertIn("message", response.data)

    @patch("blog.views.User.objects")
    def test_create_user(self, mock_objects):
        mock_objects.filter.return_value.exists.return_value = False

        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.username = "mocked"
        mock_user.email = "mocked@example.com"
        mock_objects.create.return_value = mock_user

        data = {"username": "mocked", "password": "pwd", "email": "mocked@example.com"}
        response = self.client.post("/api/user", data, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["id"], 1)

    @patch("blog.views.User.objects.get")
    def test_get_user_success(self, mock_get):
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.username = "mocked"
        mock_user.email = "mocked@example.com"
        mock_get.return_value = mock_user

        response = self.client.get("/api/user", {"username": "mocked"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["id"], 1)
        self.assertEqual(response.data["username"], "mocked")
        self.assertEqual(response.data["email"], "mocked@example.com")

    @patch("blog.views.User.objects.get")
    def test_get_user_not_found(self, mock_get):
        from blog.models import User
        mock_get.side_effect = User.DoesNotExist

        response = self.client.get("/api/user", {"username": "nope"})
        self.assertEqual(response.status_code, 404)
        self.assertIn("error", response.data)
