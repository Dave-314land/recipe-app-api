""""
Tests for User Model
"""
from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTest(TestCase):

    def test_user_has_email(self):
        """Test user has email address"""
        email = "test@example.com"
        user = get_user_model().objects.create_user(
            email=email,
            )
        self.assertEqual(user.email, email)

    def test_user_has_password(self):
        """Test user has password"""
        password = 'Mypass123'
        email = "test@example.com"
        user = get_user_model().objects.create_user(
            password=password,
            email=email,
            )
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normalized(self):
        """Test email is normalized for new users"""
        sample_emails = [
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.COM', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email, expected_email in sample_emails:
            user = get_user_model().objects.create_user(
                email=email,
                password='sample123',
                )
            self.assertEqual(user.email, expected_email)

    def test_new_user_without_email_raises_error(self):
        """Test that creating a user without an email raises a ValueError"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(
                email='',
                password='test123',
            )

    def test_create_staff(self):
        """Test creating a staff user"""
        user = get_user_model().objects.create_user(
            email='test@example.com',
            password='test123',
        )
        self.assertTrue(user.is_staff)

    def test_create_superuser(self):
        """Test creating a superuser"""
        user = get_user_model().objects.create_superuser(
            email='test@example.com',
            password='test123',
        )
        self.assertTrue(user.is_superuser)
