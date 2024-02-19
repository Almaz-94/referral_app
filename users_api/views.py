import string
import random

from rest_framework.generics import CreateAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework_simplejwt.views import TokenObtainPairView

from users_api.models import User
from users_api.permissions import IsOwner
from users_api.serializers import UserSerializer, MyTokenObtainPairSerializer, UserProfileSerializer, \
    UserUpdateSerializer


class UserCreateAPIView(CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)

        invite_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        duplicate = User.objects.filter(invite_code=invite_code).exists()
        while duplicate:
            invite_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            duplicate = User.objects.filter(invite_code=invite_code).exists()
        instance.invite_code = invite_code
        instance.save()


class UserRetrieveAPIView(RetrieveAPIView):
    serializer_class = UserProfileSerializer
    queryset = User.objects.all()


class UserUpdateAPIView(UpdateAPIView):
    serializer_class = UserUpdateSerializer

    def perform_update(self, serializer):
        instance = serializer.save()  #self.get_object()
        if User.objects.filter(invite_code=self.request.data.get("referral_code")).exists():
            instance.referred_by = User.objects.get(invite_code=self.request.data.get("referral_code"))
            instance.referral_code = self.request.data.get("referral_code")

        instance.save()
    queryset = User.objects.all()
    #permission_classes = [IsOwner]


class MyTokenObtainPairView(TokenObtainPairView):
    """View for obtaining authorization token"""
    serializer_class = MyTokenObtainPairSerializer
