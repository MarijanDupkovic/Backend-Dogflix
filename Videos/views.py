from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from .models import CategoryItem, VideoItem
from .serializers import CategoryItemSerializer, VideoItemSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.core.cache import cache
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

class CategoryItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = CategoryItemSerializer
    queryset = CategoryItem.objects.all()

class VideoItemViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    serializer_class = VideoItemSerializer
    queryset = VideoItem.objects.all()
  
    def get_queryset(self):

     queryset = cache.get('videoList')
     if not queryset:
           queryset = VideoItem.objects.all()
           cache.set('videoList', queryset, CACHE_TTL)

     return queryset
  	   



