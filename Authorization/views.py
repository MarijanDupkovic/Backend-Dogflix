import random
from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken, APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.permissions import AllowAny
from Authorization.serializers import LoginSerializer, RegistrationSerializer
from Authorization.utils import send_register_mail_to_newuser
from user.models import CustomUser
from django.core.mail import send_mail


class LoginView(ObtainAuthToken):
    
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            userData = serializer.validated_data
            if userData['email']:
                try:
                    user = get_user_model().objects.get(email=userData['email'])
                    token, created = Token.objects.get_or_create(user=user)
                    return Response({'token': token.key, 'user_id': user.pk, 'email': user.email})    
                except user.DoesNotExist:
                    return Response('User not found', status=status.HTTP_404_NOT_FOUND)
            else:
                return Response('Email field is required', status=status.HTTP_400_BAD_REQUEST)
                  
        else:
            userData = serializer.data
            if serializer.data.get('email'):
                try:
                    user = get_user_model().objects.get(email=userData['email'])
                    if not user.is_active:
                        return Response('Email not activated!',status=status.HTTP_403_FORBIDDEN)
                    else:
                        return Response('Wrong username or password',status=status.HTTP_401_UNAUTHORIZED)
                except get_user_model().DoesNotExist:
                    return Response('User not found', status=status.HTTP_404_NOT_FOUND)
            else:
                return Response('Email field is required', status=status.HTTP_400_BAD_REQUEST)

   
class RegistrationView(APIView):
    serializer_class = RegistrationSerializer
    def post(self, request, *args, **kwargs):
            serializer = RegistrationSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()

                user = get_user_model().objects.get(email=serializer.validated_data['email'])
                token, created = Token.objects.get_or_create(user=user)
                send_register_mail_to_newuser(user, token)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            
            if 'email' in serializer.errors or 'username' in serializer.errors:
                return Response('Email or username already known', status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                 

        

