from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from graphql_jwt.utils import jwt_encode, jwt_payload
# from django.conf import settings

import graphene
from graphene_django import DjangoObjectType
from .models import User
from users.send_email import send_confirmation_email


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()


class CreateUser(graphene.Mutation):
    user = graphene.Field(UserType)
    message = graphene.String()

    class Arguments:
        username = graphene.String(required=False)
        password = graphene.String(required=True)
        email = graphene.String(required=True)
        kind = graphene.String(required=False)

    def mutate(self, info, username, password, email):
        user = get_user_model()(
            username=username,
            email=email,
        )
        user.set_password(password)
        user.save()
        send_confirmation_email(email=user.email, username=user.username)

        return CreateUser(user=user, message="Successfully created user, {}".format(user.username))

class LoginUser(graphene.Mutation):
    user = graphene.Field(UserType)
    message = graphene.String()
    token = graphene.String()
    verification_prompt = graphene.String()

    class Arguments:
        email = graphene.String()
        password = graphene.String()

    def mutate(self, info, **kwargs):
        email = kwargs.get('email')
        password = kwargs.get('password')
        user = authenticate(username=email, password=password)
        error_message = 'Invalid login credentials'
        success_message = "You logged in successfully."
        verification_error = 'Your email is not verified'
        if user:
            if user.is_verified:
                payload = jwt_payload(user)
                token = jwt_encode(payload)
                return LoginUser(token=token, message=success_message, user=user)
            return LoginUser(message=verification_error)
        return LoginUser(message=error_message)



class Mutation(graphene.ObjectType):
    create_user = CreateUser.Field()
    login_user = LoginUser.Field()


class Query(graphene.ObjectType):
    me = graphene.Field(UserType)
    users = graphene.List(UserType)
    user = graphene.Field(UserType, id=graphene.Int())

    def resolve_users(self, info):
        return get_user_model().objects.all()

    def resolve_me(self, info):
        user = info.context.user
        if user.is_anonymous:
            raise Exception('Not logged in!')

        return user

    def resolve_user(self, info, **kwargs):
        id = kwargs.get('id')

        if id is not None:
            return User.objects.get(pk=id)

        return None
