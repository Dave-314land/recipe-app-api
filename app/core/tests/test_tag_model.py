""""
Tests for Tag Model
"""
from django.test import TestCase
from django.contrib.auth import get_user_model

from core import models


class TagModelTest(TestCase):
    """Test Tag Model"""

    def test_create_tag(self):
        """Test creating tag is successful"""
        user = get_user_model().objects.create_user(
            'test@example.com',
            'testpass123',
        )
        tag = models.Tag.objects.create(
            user=user,
            name='First Tag'
        )

        self.assertEqual(str(tag), tag.name)
