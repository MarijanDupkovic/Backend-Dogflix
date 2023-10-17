from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from .models import CategoryItem
from .serializers import CategoryItemSerializer
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.cache import cache
from .models import VideoItem
from .serializers import VideoItemSerializer

class CategoryItemViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.token = Token.objects.create(user=self.user)

        self.category_item1 = CategoryItem.objects.create(name='Item 1')
        self.category_item2 = CategoryItem.objects.create(name='Item 2')

    def test_list_category_items(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        response = self.client.get('/categories/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(len(response.data), CategoryItem.objects.count())

    def test_retrieve_category_item(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        response = self.client.get(f'/categories/{self.category_item1.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        serializer = CategoryItemSerializer(self.category_item1)
        self.assertEqual(response.data, serializer.data)

    def test_create_category_item(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        data = {
            'name': 'New Item',
            'description': 'New Description',
        }
        
        response = self.client.post('/categories/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertTrue(CategoryItem.objects.filter(name='New Item').exists())

    def test_update_category_item(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        data = {
            'name': 'Updated Item',
            'description': 'Updated Description',
        }
        
        response = self.client.put(f'/categories/{self.category_item1.pk}/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.category_item1.refresh_from_db()
        self.assertEqual(self.category_item1.name, 'Updated Item')

    def test_delete_category_item(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        response = self.client.delete(f'/categories/{self.category_item1.pk}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        self.assertFalse(CategoryItem.objects.filter(pk=self.category_item1.pk).exists())



class VideoItemViewSetTestCase(APITestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', email='test@example.com', password='testpassword')
        self.token = Token.objects.create(user=self.user)

        category_item = CategoryItem.objects.create(name='Category 1')

        self.video_item1 = VideoItem.objects.create(
            title='Video 1',
            description='Description 1',
            category=category_item,
            author='Author 1',
            video_file='./media/test.mp4'
        )
        self.video_item2 = VideoItem.objects.create(
            title='Video 2',
            description='Description 2',
            category=category_item,
            author='Author 2',
            video_file='./media/test2.mp4'

        )

    def test_list_video_items(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        response = self.client.get('/videos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(len(response.data), VideoItem.objects.count())

    def test_cache_video_items(self):
        self.assertIsNone(cache.get('videoList'))
        
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        
        response = self.client.get('/videos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertIsNotNone(cache.get('videoList'))
        
        response = self.client.get('/videos/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        self.assertEqual(len(response.data), VideoItem.objects.count())


    def test_retrieve_video_item(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

        response = self.client.get(f'/videos/{self.video_item1.pk}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_data = {
            'id': self.video_item1.id,
            'title': self.video_item1.title,
            'description': self.video_item1.description,
            'category': self.video_item1.category.id,  
            'author': self.video_item1.author,
        }

        expected_video_url = 'http://testserver/media/media/test.mp4'  

        self.assertEqual(response.data['video_file'], expected_video_url)
        self.assertDictContainsSubset(expected_data, response.data)

    def test_create_video_item(self):
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')
        uploaded_file = SimpleUploadedFile("test3.mp4", b"file_content", content_type="video/mp4")
        data = {
            "title": "New Video",
            "description": "New Description",
            "category": self.video_item1.category.id,
            "author": "New Author",
            "video_file":uploaded_file
        }
        
        response = self.client.post('/videos/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        self.assertTrue(VideoItem.objects.filter(title='New Video').exists())

