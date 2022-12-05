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
            'password': 'Testpass123',
            'name': 'Test name',
        }
        self.response = self.client.post(CREATE_USER_URL, self.payload)

    def test_create_user_success(self):
        """Test creating the user is successfull"""
        response = self.response
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_user_has_password(self):
        """Test user created with password"""
        payload = self.payload
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))

    def test_user_password_is_not_in_response_data(self):
        """Test response data does not contain password"""
        response = self.response
        self.assertNotIn('password', response.data)

    def test_user_password_meets_minimum_length(self):
        "Test user password meets minimum length requirement"
        min_length = 8
        payload = self.payload
        user = get_user_model().objects.get(email=payload['email'])
        self.assertGreaterEqual(len(user.password), min_length,)

    def test_user_has_name(self):
        """Test user created with name"""
        payload = self.payload
        user = get_user_model().objects.get(email=payload['email'])
        expected_user_name = 'Test name'
        self.assertEqual(str(user.name), expected_user_name)
