from rest_framework import serializers

from .models import CategoryItem, VideoItem

class CategoryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryItem
        fields = '__all__'

class VideoItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoItem
        fields = ('id','title', 'description', 'category','author','video_file','video_file_480p','video_file_720p','video_file_1080p','created_at')
       
