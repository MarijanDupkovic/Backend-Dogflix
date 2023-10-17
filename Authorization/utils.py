from django.conf import settings
from django.core.mail import send_mail
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.dispatch import receiver
from user.models import CustomUser
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

def send_register_mail_to_newuser(user,token):
    context = {'username': user.username, 'token': token}
    rendered = render_to_string("auth/signup.html", context)
    subject = 'Welcome to Dogflix'
    html_message = rendered
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email]
    
    send_mail(subject, '',  email_from, recipient_list, html_message=html_message)

@api_view(('GET',))
def activate_user(request, token):
    user = get_object_or_404(CustomUser, auth_token=token)
    user.is_active = True
    user.save()
    return Response({'message': 'User activated successfully.'})

@api_view(('GET',))
def logout_user(request, token):
    token_to_delete = get_object_or_404(Token, key=token)
    token_to_delete.delete()
    
    return Response({'message': 'User logged out successfully.'})


def change_password(username, pw1, pw2):
    if pw1 != pw2:
        raise Exception("pw1 not equal to pw2")

    user = CustomUser.objects.get(username=username)

    user.set_password(pw1)

    send_mail(
        "Your password was changed successfully",

        [user.email],
        fail_silently=False,
    )

    user.save()