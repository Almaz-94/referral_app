import string
import random

from users_api.models import User


def check_verification_number():
    pass

def generate_invite_code():
    invite_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    is_duplicate = User.objects.filter(invite_code=invite_code).exists()
    while is_duplicate:
        invite_code = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        is_duplicate = User.objects.filter(invite_code=invite_code).exists()
    return invite_code
