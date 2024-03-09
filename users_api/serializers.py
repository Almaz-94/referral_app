from rest_framework import serializers
from rest_framework.serializers import ModelSerializer
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from users_api.models import User
from users_api.validators import ReferralCodeValidator, PhoneNumberValidator


class UserSerializer(ModelSerializer):
    """ Serializer for User creation """
    class Meta:
        model = User
        fields = ['phone_number', 'authorization_code']
        validators = [PhoneNumberValidator('phone_number'), ]


class UserLoginSerializer(serializers.Serializer):
    """
    This serializer defines two fields for authentication:
      * phone_number
      * authorization_code.
    It will try to authenticate the user with when validated.
    """
    phone_number = serializers.CharField()
    authorization_code = serializers.CharField()


class UserPhoneNumberSerializer(ModelSerializer):
    """ This serializer is used for displaying invited_users in user's profile """
    class Meta:
        model = User
        fields = ['phone_number']


class UserProfileSerializer(ModelSerializer):
    """ Serializer for retrieving user's profile """
    invited_users = UserPhoneNumberSerializer(source='user_set', many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'phone_number', 'referral_code', 'referred_by', 'invite_code', 'invited_users']



class UserUpdateSerializer(ModelSerializer):
    """ Serializer for updating user's referral_code in his profile """
    class Meta:
        model = User
        fields = ['referral_code']
        validators = [ReferralCodeValidator('referral_code'), ]

