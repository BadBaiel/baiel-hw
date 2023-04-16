from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import UserLoginValidateSerializer, UserCreateValidateSerializer, ConfirmCodeValidateSerializer
from django.contrib.auth.models import User
from .models import ConfirmUserCode

@api_view(['POST'])
def authorization_api_view(request):
    serializer = UserLoginValidateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = authenticate(**serializer.validated_data)
    if user:
        token, created = Token.objects.get_or_create(user=user)
        return Response(data={'key': token.key})
    return Response(status=status.HTTP_401_UNAUTHORIZED,
                    data={'error': 'Username or Password wrong!'})

@api_view(['POST'])
def registration_api_view(request):
    serializer = UserCreateValidateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = User.objects.create_user(**serializer.validated_data)
    return Response(status=status.HTTP_201_CREATED,
                    data={'user_id': user.id})

@api_view(['POST'])
def confirm_api_view(request):
    serializer = ConfirmCodeValidateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    try:
        if ConfirmUserCode.objects.filter(code=request.data['code']):
            User.objects.update(is_active=True)
            return Response(status=status.HTTP_202_ACCEPTED,
                            data={'success': 'confirmed'})

        return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                        data={'error': 'wrong id or code!'})

    except ValueError:
        return Response(status=status.HTTP_406_NOT_ACCEPTABLE,
                        data={'error': 'write code number!'})