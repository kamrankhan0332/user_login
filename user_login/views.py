from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import SingUpSerializer, LogInSerializer
from .models import User
from rest_framework import exceptions
import datetime
import jwt
from django.conf import settings


@api_view(['POST'])
def sign_up(request):
    try:
        if request.method == 'POST':
            data = request.data['value']
            user = User.objects.create(username=data['username'], email=data['email'])
            user.set_password(data['password'])
            user.save()
            data['user'] = user.id
            serializer = SingUpSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
            return Response(status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"Error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


def generate_access_token(user):
    access_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, minutes=60),
        'iat': datetime.datetime.utcnow(),
    }
    access_token = jwt.encode(access_token_payload,
                              settings.SECRET_KEY, algorithm='HS256')
    return access_token


def generate_refresh_token(user):
    refresh_token_payload = {
        'user_id': user.id,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7),
        'iat': datetime.datetime.utcnow()
    }
    refresh_token = jwt.encode(refresh_token_payload, settings.REFRESH_TOKEN_SECRET, algorithm='HS256')
    return refresh_token


@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    response = Response()
    if (username is None) or (password is None):
        raise exceptions.AuthenticationFailed(
            'username and password required')

    user = User.objects.filter(username=username).first()
    if user is None:
        raise exceptions.AuthenticationFailed('user not found')
    if not user.check_password(password):
        raise exceptions.AuthenticationFailed('wrong password')

    serialized_user = LogInSerializer(user).data

    access_token = generate_access_token(user)
    refresh_token = generate_refresh_token(user)

    response.set_cookie(key='refreshtoken', value=refresh_token, httponly=True)
    response.data = {
        'access_token': access_token,
        'user': serialized_user,
    }
    return response


@api_view(['POST'])
def refresh_token_view(request):
    refresh_token = request.COOKIES.get('refreshtoken')
    if refresh_token == 'None':
        raise exceptions.AuthenticationFailed(
            'PLease login')
    try:
        payload = jwt.decode(
            refresh_token, settings.REFRESH_TOKEN_SECRET, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise exceptions.AuthenticationFailed(
            'expired refresh token, please login again.')

    user = User.objects.filter(id=payload.get('user_id')).first()
    if user is None:
        raise exceptions.AuthenticationFailed('User not found')

    if not user.is_active:
        raise exceptions.AuthenticationFailed('user is inactive')

    access_token = generate_access_token(user)
    return Response({'access_token': access_token})


@api_view(['POST'])
def logout_view(request):
    response = Response()
    response.set_cookie(key='refreshtoken', value=None, httponly=True)
    response.data = {
        'access_token': '',
        'user': '',
    }
    return response
