from django.shortcuts import render
import jwt

# from django.conf.settings.AUTH_USER_MODEL import User
from django.conf import settings
# from django.conf.settings import SECRET_KEY, DOMAIN

# Create your views here.


def activate_account(request, token):
    username = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])["user"]
    user = settings.AUTH_USER_MODEL.objects.get(username=username)
    if username and not user.is_verified:
        user.is_verified = True
        user.save()
        return redirect(f'{settings.DOMAIN}/graphql/')
