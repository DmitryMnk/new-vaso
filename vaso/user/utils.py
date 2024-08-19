from django.contrib.auth.models import User
import requests
from main.amocrm import create_contact
from user.models import UserProfile


def get_of_create_user(phone: str, name: str) -> UserProfile:
    if UserProfile.objects.filter(phone_number=phone).exists():
        profile: UserProfile = UserProfile.objects.get(phone_number=phone)
        return profile

    data = {
        'phone': phone,
        'name': name
    }

    contact_id = create_contact(data).get("_embedded").get("contacts")[0].get('id')

    new_user = User.objects.create_user(username=phone, first_name=name)
    new_profile = UserProfile.objects.create(
        user=new_user,
        phone_number=phone,
        amo_id=contact_id,
    )

    return new_profile

