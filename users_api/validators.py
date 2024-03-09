import phonenumbers
from rest_framework.exceptions import ValidationError

from users_api.models import User


class ReferralCodeValidator:
    """ Validator for checking 'referral_code' existence in database"""
    def __init__(self, referral_code):
        self.referral_code = referral_code

    def __call__(self, value):
        ref_code = dict(value).get(self.referral_code)
        if not User.objects.filter(invite_code=ref_code).exists():
            raise ValidationError(f'Referral code "{ref_code}" does not exist')
        return


class PhoneNumberValidator:
    """ Phone number validator """
    def __init__(self, phone_number):
        self.phone_number = phone_number

    def __call__(self, value):
        string_number = str(dict(value).get(self.phone_number))
        try:
            parsed_number = phonenumbers.parse(string_number)
            if not phonenumbers.is_valid_number(parsed_number):
                raise ValidationError(f'Enter a valid phone number')
        except Exception:
            raise ValidationError(f'Enter a valid phone number')
