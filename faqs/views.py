from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import logout
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.core.cache import cache
from django.conf import settings
import logging
from .models import FAQ
from .serializers import FAQSerializer

logger = logging.getLogger(__name__)

def home(request):
    """
    Home page view that displays all FAQs
    """
    try:
        # Get language from query params, default to English
        lang = request.GET.get('lang', 'en')
        
        # Try to get FAQs from cache
        cache_key = f'home_faqs_{lang}'
        faqs = cache.get(cache_key)
        
        if faqs is None:
            # If not in cache, get from database
            faqs = FAQ.objects.all().order_by('-created_at')
            
            # Translate FAQs if needed
            if lang != 'en':
                for faq in faqs:
                    faq.question = faq.get_question(lang)
                    faq.answer = faq.get_answer(lang)
            
            # Cache the results
            try:
                cache.set(cache_key, faqs, timeout=3600)
            except Exception as e:
                logger.warning(f"Failed to cache FAQs: {str(e)}")
        
        context = {
            'faqs': faqs,
            'current_language': lang,
        }
        
        return render(request, 'faqs/home.html', context)
        
    except Exception as e:
        logger.error(f"Error in home view: {str(e)}")
        messages.error(request, "An error occurred while loading the FAQs. Please try again later.")
        return render(request, 'faqs/home.html', {'faqs': []})

def custom_logout(request):
    """Custom logout view that works with both GET and POST"""
    logout(request)
    messages.success(request, 'You have been successfully logged out.')
    return redirect('home')

class FAQViewSet(viewsets.ModelViewSet):
    queryset = FAQ.objects.all()
    serializer_class = FAQSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = None  # Disable pagination for simplicity

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [permissions.IsAdminUser]
        else:
            permission_classes = [permissions.AllowAny]
        return [permission() for permission in permission_classes]

    def get_queryset(self):
        try:
            return FAQ.objects.all().order_by('-created_at')
        except Exception as e:
            logger.error(f"Error fetching FAQs: {str(e)}")
            return FAQ.objects.none()

    def list(self, request, *args, **kwargs):
        try:
            # Get language from query params, default to English
            lang = request.query_params.get('lang', 'en')
            
            # Get FAQs
            queryset = self.get_queryset()
            
            # Try to get from cache first
            cache_key = f'faq_list_{lang}'
            cached_data = None
            
            try:
                cached_data = cache.get(cache_key)
            except Exception as e:
                logger.warning(f"Cache get failed: {str(e)}")

            if cached_data:
                return Response(cached_data)

            # Prepare data with translations
            data = []
            for faq in queryset:
                try:
                    item = {
                        'id': faq.id,
                        'question': faq.get_question(lang),
                        'answer': faq.get_answer(lang),
                        'created_at': faq.created_at,
                        'updated_at': faq.updated_at
                    }
                    data.append(item)
                except Exception as e:
                    logger.error(f"Error processing FAQ {faq.id}: {str(e)}")
                    continue

            # Try to cache the results
            try:
                cache.set(cache_key, data, timeout=3600)
            except Exception as e:
                logger.warning(f"Cache set failed: {str(e)}")

            return Response(data)

        except Exception as e:
            logger.error(f"Error in FAQ list view: {str(e)}")
            return Response(
                {'error': 'Unable to fetch FAQs'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def create(self, request, *args, **kwargs):
        try:
            response = super().create(request, *args, **kwargs)
            # Clear cache on creation
            self._clear_cache()
            return response
        except Exception as e:
            logger.error(f"Error creating FAQ: {str(e)}")
            return Response(
                {'error': 'Unable to create FAQ'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def update(self, request, *args, **kwargs):
        try:
            response = super().update(request, *args, **kwargs)
            # Clear cache on update
            self._clear_cache()
            return response
        except Exception as e:
            logger.error(f"Error updating FAQ: {str(e)}")
            return Response(
                {'error': 'Unable to update FAQ'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def destroy(self, request, *args, **kwargs):
        try:
            response = super().destroy(request, *args, **kwargs)
            # Clear cache on deletion
            self._clear_cache()
            return response
        except Exception as e:
            logger.error(f"Error deleting FAQ: {str(e)}")
            return Response(
                {'error': 'Unable to delete FAQ'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

    def _clear_cache(self):
        """Clear all FAQ-related caches"""
        try:
            for lang in ['en', 'hi', 'bn']:
                cache.delete(f'faq_list_{lang}')
        except Exception as e:
            logger.warning(f"Cache clear failed: {str(e)}")
