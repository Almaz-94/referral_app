from random import randint

from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users_api.models import User


class UserSerializer(ModelSerializer):
    authorization_code = serializers.SerializerMethodField()

    def get_authorization_code(self, obj):
        return randint(1000, 9999)

    class Meta:
        model = User
        fields = ['username', 'phone_number', 'password', 'authorization_code']


class UserPhoneNumberSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number']


class UserProfileSerializer(ModelSerializer):
    invited_users = UserPhoneNumberSerializer(source='user_set', many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'phone_number', 'referral_code', 'referred_by', 'invite_code', 'invited_users']


class UserUpdateSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ['referred_by']


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        return token
