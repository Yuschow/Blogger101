from django.test import TestCase
from unittest.mock import patch, MagicMock
from rest_framework.test import APIClient

class GroupAPITEST(TestCase):
    def setUp(self):
        self.client = APIClient()
    
    @patch("blog.views.Group.objects")
    def test_post_group_success(self, mock_objects):
