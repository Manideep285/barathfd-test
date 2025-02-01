from django.db import models
from django.core.cache import cache
from django.utils.translation import gettext_lazy as _
from ckeditor.fields import RichTextField
from googletrans import Translator, LANGUAGES
import logging
import json

logger = logging.getLogger(__name__)

LANGUAGE_CHOICES = [
    ('en', 'English'),
    ('hi', 'Hindi'),
    ('bn', 'Bengali'),
]

class FAQ(models.Model):
    question = models.TextField(_('Question'))
    answer = RichTextField(_('Answer'))
    question_hi = models.TextField(_('Question (Hindi)'), blank=True, null=True)
    question_bn = models.TextField(_('Question (Bengali)'), blank=True, null=True)
    answer_hi = RichTextField(_('Answer (Hindi)'), blank=True, null=True)
    answer_bn = RichTextField(_('Answer (Bengali)'), blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _('FAQ')
        verbose_name_plural = _('FAQs')
        ordering = ['-created_at']

    def __str__(self):
        return self.question[:50]

    def _safe_cache_get(self, cache_key):
        """Safely get value from cache with error handling"""
        try:
            return cache.get(cache_key)
        except Exception as e:
            logger.warning(f"Cache get failed for key {cache_key}: {str(e)}")
            return None

    def _safe_cache_set(self, cache_key, value):
        """Safely set value in cache with error handling"""
        try:
            cache.set(cache_key, value, timeout=3600)  # 1 hour cache
            return True
        except Exception as e:
            logger.warning(f"Cache set failed for key {cache_key}: {str(e)}")
            return False

    def _safe_translate(self, text, dest_lang):
        """Safely translate text with error handling and retry"""
        if not text:
            return ""
            
        try:
            translator = Translator()
            translation = translator.translate(text, dest=dest_lang)
            return translation.text if translation else text
        except Exception as e:
            logger.error(f"Translation failed: {str(e)}")
            return text

    def get_translation(self, field, lang):
        """Get translated text with caching and fallback to English"""
        if lang == 'en':
            return getattr(self, field)

        if lang not in ['hi', 'bn']:
            logger.warning(f"Unsupported language: {lang}")
            return getattr(self, field)

        # Try to get from model first
        translated_field = f'{field}_{lang}'
        translated_value = getattr(self, translated_field)
        if translated_value:
            return translated_value

        # Try to get from cache
        cache_key = f'faq_{self.id}_{field}_{lang}'
        cached_value = self._safe_cache_get(cache_key)
        if cached_value:
            return cached_value

        # Translate and cache
        original_text = getattr(self, field)
        translated_text = self._safe_translate(original_text, lang)
        
        if translated_text != original_text:
            # Only cache and save if translation was successful
            self._safe_cache_set(cache_key, translated_text)
            setattr(self, translated_field, translated_text)
            try:
                self.save(update_fields=[translated_field])
            except Exception as e:
                logger.error(f"Failed to save translation: {str(e)}")

        return translated_text

    def get_question(self, lang='en'):
        """Get translated question"""
        return self.get_translation('question', lang)

    def get_answer(self, lang='en'):
        """Get translated answer"""
        return self.get_translation('answer', lang)

    def save(self, *args, **kwargs):
        """Override save to handle translations"""
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new:
            # Queue translations for new FAQs
            for lang in ['hi', 'bn']:
                try:
                    if not getattr(self, f'question_{lang}'):
                        translated_q = self._safe_translate(self.question, lang)
                        setattr(self, f'question_{lang}', translated_q)
                    
                    if not getattr(self, f'answer_{lang}'):
                        translated_a = self._safe_translate(self.answer, lang)
                        setattr(self, f'answer_{lang}', translated_a)
                    
                    self.save(update_fields=[
                        f'question_{lang}',
                        f'answer_{lang}'
                    ])
                except Exception as e:
                    logger.error(f"Failed to translate new FAQ to {lang}: {str(e)}")
                    # Continue with other languages
