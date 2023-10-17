from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from .utils import send_register_mail_to_newuser
from django.core import mail
class LoginViewTest(APITestCase):
    def setUp(self):
        self.user_data = {
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'username': 'testuser'
        }
        self.user = get_user_model().objects.create_user(**self.user_data)
        self.login_url = reverse('login')  

    def test_login_valid_user(self):
        response = self.client.post(self.login_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertIn('user_id', response.data)
        self.assertEqual(response.data['email'], self.user_data['email'])

    def test_login_invalid_user_inactive(self):
        self.user.is_active = False
        self.user.save()
        response = self.client.post(self.login_url, self.user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data, 'Email not activated!')

    def test_login_invalid_user_wrong_credentials(self):
        invalid_user_data = {
            'email': 'testuser@example.com',
            'password': 'wrongpassword'
        }
        response = self.client.post(self.login_url, invalid_user_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data, 'Wrong username or password')
    
    def test_login_no_data(self):
        response = self.client.post(self.login_url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_missing_email(self):
        invalid_user_data = {
            'password': 'testpassword'
        }
        response = self.client.post(self.login_url, invalid_user_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_with_missing_password(self):
        invalid_user_data = {
            'email': 'testuser@example.com'
        }
        response = self.client.post(self.login_url, invalid_user_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_with_wrong_email(self):
        invalid_user_data = {
            'email': 'nonexistent@example.com',
            'password': 'testpassword'
        }
        response = self.client.post(self.login_url, invalid_user_data)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_login_with_blank_password(self):
        invalid_user_data = {
            'email': 'testuser@example.com',
            'password': ''
        }
        response = self.client.post(self.login_url, invalid_user_data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class RegistrationViewTestCase(APITestCase):
    def setUp(self):
        # Create a test user
        self.user = get_user_model().objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword',
        )
   
    def test_successful_registration(self):
        data = {
            "username": "testuser1",
            "email": "testing@example.com",
            "password": "testpassword",
            "password2":"testpassword"
        }
        response = self.client.post('/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(get_user_model().objects.filter(username="testuser").count(), 1)

    def test_registration_with_known_email_or_username(self):
        # Create a user with a known email or username
        get_user_model().objects.create_user(username="existinguser", email="existing@example.com", password="existingpassword")

        data = {
            "username": "existinguser",
            "email": "test@example.com",
            "password": "testpassword"
        }
        ##
        response = self.client.post('/register/', data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, "Email or username already known")




