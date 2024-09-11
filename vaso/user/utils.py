import hashlib
import json
import time
from datetime import datetime
import requests
import phonenumbers
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpRequest, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from rest_framework.request import Request
from main.amocrm import create_contact
from user.models import UserProfile
from vaso import settings


ALLOWED_IPS = [
    '37.9.15.244',
    '5.188.131.157',
    '5.188.131.158',
    '82.202.237.68'
]

def get_or_create_user(phone: str, name: str = None) -> UserProfile:
    if UserProfile.objects.filter(phone_number=phone).exists():
        profile: UserProfile = UserProfile.objects.get(phone_number=phone)
        return profile

    if not name:
        name = 'Клиент'

    data = {
        'phone': phone,
        'name': name
    }

    contact_id = create_contact(data).get("_embedded").get("contacts")[0].get('id')
    print(contact_id)
    new_user = User.objects.create_user(username=phone, first_name=name)
    new_profile = UserProfile.objects.create(
        user=new_user,
        phone_number=phone,
        amo_id=contact_id,
    )

    return new_profile

def authorize_user(profile: UserProfile, request: Request) -> None:
    user = profile.user
    request.session.flush()
    login(request, user)


def send_code(phone: str, code: int):
    parsed_number = phonenumbers.parse(phone, "RU")
    phone_number = phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)

    ts = str(time.time())
    secret = hashlib.md5((ts + settings.REDSMS_KEY).encode()).hexdigest()

    headers = {
        'login': settings.REDSMS_LOGIN,
        'ts': ts,
        'secret': secret,
        'Content-type': 'application/json',
    }
    data = {
        'route': 'fcall',
        'to': phone_number,
        'text': code,
    }
    response = requests.post('https://cp.redsms.ru/api/message', headers=headers, data=json.dumps(data))
    print(response.json())

@csrf_exempt
def webhook_code(request: HttpRequest) -> HttpResponse:
    ip_addr = request.META.get('REMOTE_ADDR')

    if not settings.DEBUG and (ip_addr not in ALLOWED_IPS):
        return HttpResponseForbidden("Forbidden")

    return HttpResponse(status=200)
