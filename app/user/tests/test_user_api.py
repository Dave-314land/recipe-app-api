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

    def test_user_with_email_exists_error(self):
        """Test error returned if user with email exists"""
        new_payload = {
            'email': 'test@example.com',
            'password': 'Testpass123',
            'name': 'Test name',
        }
        response = self.client.post(CREATE_USER_URL, new_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_has_password(self):
        """Test user created with password"""
        payload = self.payload
        user = get_user_model().objects.get(email=payload['email'])
        self.assertTrue(user.check_password(payload['password']))

    def test_user_password_is_not_in_response_data(self):
        """Test response data does not contain password"""
        response = self.response
        self.assertNotIn('password', response.data)

    def test_user_password_too_short_error(self):
        "Test error returned if password does not meet min length"
        bad_payload = {
            'email': 'test1@example.com',
            'password': 'short',
            'name': 'Test name',
        }
        response = self.client.post(CREATE_USER_URL, bad_payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_user_with_short_password_not_created(self):
        "Test user does not exist if password does not meet min length"
        bad_payload = {
            'email': 'test1@example.com',
            'password': 'short',
            'name': 'Test name',
        }
        self.client.post(CREATE_USER_URL, bad_payload)
        bad_user = get_user_model().objects.filter(
            email=bad_payload['email']
            ).exists()
        self.assertFalse(bad_user)

    def test_user_has_name(self):
        """Test user created with name"""
        payload = self.payload
        user = get_user_model().objects.get(email=payload['email'])
        expected_user_name = 'Test name'
        self.assertEqual(str(user.name), expected_user_name)