import pytest
from django.test import TestCase
from faqs.models import FAQ
from django.core.cache import cache

class TestFAQModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.faq = FAQ.objects.create(
            question="What is this?",
            answer="This is a test FAQ.",
        )

    def setUp(self):
        cache.clear()

    def test_faq_creation(self):
        self.assertEqual(self.faq.question, "What is this?")
        self.assertEqual(self.faq.answer, "This is a test FAQ.")

    def test_str_representation(self):
        self.assertEqual(str(self.faq), "What is this?")

    def test_translation_fallback(self):
        # When translation is not available in cache, it should attempt to translate
        translated_question = self.faq.get_question('hi')
        # Just verify that we get some non-empty string back
        self.assertTrue(isinstance(translated_question, str))
        self.assertTrue(len(translated_question) > 0)

    def test_cache_mechanism(self):
        # Test cache setting and getting
        cache_key = f'faq_{self.faq.id}_question_hi'
        test_value = "यह क्या है?"
        self.faq._safe_cache_set(cache_key, test_value)
        self.assertEqual(self.faq._safe_cache_get(cache_key), test_value)
