from django.shortcuts import render, redirect
import jwt


from django.conf import settings
from users.models import User
# from django.conf.settings import SECRET_KEY, DOMAIN

# Create your views here.


def activate_account(request, token):
    username = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])["user"]
    user = User.objects.get(username=username)

    if username and not user.is_verified:
        user.is_verified = True
        user.save()
        return redirect(f'{settings.DOMAIN}')
    return redirect(f'{settings.DOMAIN}')
