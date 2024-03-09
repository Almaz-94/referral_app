import string
import random
import time

from rest_framework import status, permissions
from rest_framework.exceptions import ValidationError
from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users_api.auth_backend import PhoneAuth
from users_api.models import User
from users_api.permissions import IsOwner
from users_api.serializers import UserSerializer, UserProfileSerializer, \
    UserUpdateSerializer, UserLoginSerializer


class UserCreateAPIView(CreateAPIView):
    """ View for User creation """
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        """ Upon creation gives User authorization_code and  unique invite_code """
        instance = serializer.save()
        invite_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        duplicate = User.objects.filter(invite_code=invite_code).exists()
        while duplicate:
            invite_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            duplicate = User.objects.filter(invite_code=invite_code).exists()
        instance.invite_code = invite_code
        instance.authorization_code = random.randint(1000, 9999)
        instance.save()

    def create(self, request, *args, **kwargs):
        """ If User exists send changed auth code else create User """
        existing_user = User.objects.filter(phone_number=request.data['phone_number']).first()
        if existing_user:
            existing_user.authorization_code = random.randint(1000, 9999)
            existing_user.save()
            response = {'phone_number': existing_user.phone_number,
                        'authorization_code': existing_user.authorization_code}
        else:
            response = super().create(request, *args, **kwargs).data

        time.sleep(2)
        return Response({'message': 'Proceed to http://localhost:8000/api/users/token/ '
                                    'Your authorization code is sent via message to your phone_number. ',
                         'authorization details': response})


class UserTokenAPIView(APIView):
    """ View for creating auth token for user """
    serializer_class = UserLoginSerializer

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            vd = serializer.validated_data
            user = PhoneAuth().authenticate(request=request, username=vd['phone_number'],
                                            password=vd['authorization_code'])
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({'access': str(refresh.access_token),'refresh': str(refresh)},
                                status=status.HTTP_200_OK)
        raise ValidationError('Your phone number or authorization code are incorrect')




class UserRetrieveAPIView(RetrieveAPIView):
    """ View for retrieving user's profile """
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, ]


class UserUpdateAPIView(UpdateAPIView):
    """ View for updating user's referral code in his profile """
    serializer_class = UserUpdateSerializer
    queryset = User.objects.all()
    permission_classes = [IsOwner]

    def perform_update(self, serializer):
        """ User cannot enter referral code twice """
        instance = self.get_object()
        if instance.referral_code:
            message = {'message': 'You cannot change your referral code twice'}
            raise ValidationError(message)
        elif instance.invite_code == self.request.data.get("referral_code"):
            message = {'message': 'You cannot set your invite code as your referral code'}
            raise ValidationError(message)
        instance.referred_by = User.objects.get(invite_code=self.request.data.get("referral_code"))
        instance.referral_code = self.request.data.get("referral_code")
        instance.save()
