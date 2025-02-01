import pytest
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from faqs.models import FAQ
from django.contrib.auth.models import User

class TestFAQViews(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='adminpass123'
        )
        self.faq = FAQ.objects.create(
            question="Test FAQ?",
            answer="Test Answer",
        )
        self.list_url = reverse('faq-list')
        self.detail_url = reverse('faq-detail', kwargs={'pk': self.faq.pk})

    def test_faq_list_get(self):
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['question'], "Test FAQ?")
        self.assertEqual(response.data[0]['answer'], "Test Answer")

    def test_faq_list_with_language(self):
        response = self.client.get(f"{self.list_url}?lang=hi")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data[0]['question'])
        self.assertIsNotNone(response.data[0]['answer'])

    def test_faq_create_authenticated(self):
        self.client.force_authenticate(user=self.user)
        data = {
            "question": "New FAQ?",
            "answer": "New Answer"
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(FAQ.objects.count(), 2)

    def test_faq_create_unauthenticated(self):
        data = {
            "question": "New FAQ?",
            "answer": "New Answer"
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(FAQ.objects.count(), 1)
