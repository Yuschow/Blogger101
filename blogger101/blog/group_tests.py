from django.test import TestCase
from unittest.mock import patch, MagicMock
from rest_framework.test import APIClient

class GroupAPITEST(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    @patch("blog.views.Group.objects")
    def test_post_group_success(self, mock_objects):
        # Mock objects.filter().exists() -> False
        mock_objects.filter.return_value.exists.return_value = False

        # Mock user instance
        mock_group = MagicMock()
        mock_group.id = 1
        mock_group.username = "test group"
        mock_group.groupcode = "test001"
        mock_objects.create.return_value = mock_group

        data = {"groupname": "test group", "groupcode": "test001", "email": "test01@example.com"}
        response = self.client.post("/api/group", data, format="json")

        self.assertEqual(response.status_code, 201)
        self.assertIn("message", response.data)

    @patch("blog.views.Group.objects")
    def test_post_group_missing_params(self, mock_ojects):
        data = {
                "groupname" : "test group"
            }
        response = self.client.post("api/group", data, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertIn("error", response.data)

    @patch("blog.views.Group.objects")
    def test_get_group_pagination(self, mock_ojects):
        mock_ojects.all.return_value = [
            MagicMock(id=1, groupname="Group 1", groupcode="G001"),
            MagicMock(id=2, groupname="Group 2", groupcode="G002"),

        ]
        response = self.client.get("/api/group", {"page": 1, "page_size":10})
        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.data)
    




