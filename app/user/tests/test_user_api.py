"""
Tests for the user API
"""

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status


CREATE_USER_URL = reverse('user:create')

def create_user(**params):
    """Create and return a new user"""
    return get_user_model().objects.create_user(**params)


class PublicUserApiTests(TestCase):
    """Test the public features of the user API"""

    def setUp(self):
        self.client = APIClient()
        self.payload = {
            'email': 'test@example.com',
        }
        self.response = self.client.post(CREATE_USER_URL, self.payload)
    
    def test_create_user_success(self):
        """Test creating the user is successfull"""
        response = self.response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
