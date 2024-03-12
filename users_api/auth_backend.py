from django.contrib.auth.backends import ModelBackend

from users_api.models import User


class PhoneAuth:
    """ Authorization backend class for custom user authentication """
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(phone_number=username, authorization_code=password)
            return user
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
