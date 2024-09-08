import http.client
from typing import Dict

from vaso import settings
import requests

PIPELINE = {
    'id': 8415650,
    'statuses': {
        'Анкета заполнена': 68497894,
        'Букет собран': 68706382,
        'Доработка букета': 68706386,
        'Оплачивают заказ': 68706390,
        'Оплачено': 68706394,
        'Поиск курьера': 68706398,
        'Передано курьеру': 68706402,
        'Доставлено': 68706406,
    },
    'fields': {
        'order_id': 901501,
        'address': 898593,
        'order_type': 906147,
        'date': 898595,
        'photo': 898587,
        'colors': 909785,
        'package': 909787,
        'else': 909789,
        'payment_url': 909841
    }
}


def create_deal_showcase(deal_data: Dict):
    deal = {
        "price": int(deal_data.get('price')),  # Сумма сделки
        "pipeline_id": PIPELINE['id'],  # ID воронки, в которую добавляется сделка
        "status_id": PIPELINE['statuses']['Оплачивают заказ'],  # ID статуса сделки в воронке
        "custom_fields_values": [
            {
                'field_id': PIPELINE['fields']['address'],
                "values": [
                    {
                        'enum_id': 1,
                        'value': deal_data.get('address')
                    }
                ]
            },
            {
                'field_id': PIPELINE['fields']['order_id'],
                "values": [
                    {
                        'value': deal_data.get('order_id')
                    }
                ]
            },
            {
                'field_id': PIPELINE['fields']['order_type'],
                "values": [
                    {
                        'value': deal_data.get('order_type')
                    }
                ]
            },
            {
                'field_id': PIPELINE['fields']['date'],
                "values": [
                    {
                        'value': deal_data.get('date')
                    }
                ]
            },
        ],
        "_embedded": {
            "contacts": [
                {
                    "id": deal_data.get('contact_id')
                }
            ]
        }
    }

    deals_url = f'https://{settings.AMOCRM_SUBDOMAIN}.amocrm.ru/api/v4/leads'
    headers = {
        'Authorization': f'Bearer {settings.AMOCRM_TOKEN}',
        'Content-Type': 'application/json',
    }

    response = requests.post(deals_url, json=[deal], headers=headers)
    print(response.json())
    return response.json()


def create_deal_ib(deal_data: Dict):
    deal = {
        "price": int(deal_data.get('price')),  # Сумма сделки
        "pipeline_id": PIPELINE['id'],  # ID воронки, в которую добавляется сделка
        "status_id": PIPELINE['statuses']['Анкета заполнена'],  # ID статуса сделки в воронке
        "custom_fields_values": [
            {
                'field_id': PIPELINE['fields']['address'],
                "values": [
                    {
                        'enum_id': 1,
                        'value': deal_data.get('address')
                    }
                ]
            },
            {
                'field_id': PIPELINE['fields']['order_id'],
                "values": [
                    {
                        'value': deal_data.get('order_id')
                    }
                ]
            },
            {
                'field_id': PIPELINE['fields']['order_type'],
                "values": [
                    {
                        'value': deal_data.get('order_type')
                    }
                ]
            },
            {
                'field_id': PIPELINE['fields']['colors'],
                "values": [
                    {
                        'value': deal_data.get('colors')
                    }
                ]
            },
            {
                'field_id': PIPELINE['fields']['package'],
                "values": [
                    {
                        'value': deal_data.get('package')
                    }
                ]
            },
            {
                'field_id': PIPELINE['fields']['else'],
                "values": [
                    {
                        'value': deal_data.get('else')
                    }
                ]
            },
            {
                'field_id': PIPELINE['fields']['date'],
                "values": [
                    {
                        'value': deal_data.get('date')
                    }
                ]
            },
        ],
        "_embedded": {
            "contacts": [
                {
                    "id": deal_data.get('contact_id')
                }
            ]
        }
    }

    deals_url = f'https://{settings.AMOCRM_SUBDOMAIN}.amocrm.ru/api/v4/leads'
    headers = {
        'Authorization': f'Bearer {settings.AMOCRM_TOKEN}',
        'Content-Type': 'application/json',
    }

    response = requests.post(deals_url, json=[deal], headers=headers)
    return response.json()


def get_pipelines():
    url = f'https://{settings.AMOCRM_SUBDOMAIN}.amocrm.ru/api/v4/leads/pipelines'
    headers = {
        'Authorization': f'Bearer {settings.AMOCRM_TOKEN}',
    }
    response = requests.get(url, headers=headers)
    print(response.json())
    return response.json()

def create_contact(data: Dict) -> Dict:
    url = f'https://{settings.AMOCRM_SUBDOMAIN}.amocrm.ru/api/v4/contacts'
    headers = {
        'Authorization': f'Bearer {settings.AMOCRM_TOKEN}',
        'Content-Type': 'application/json',
    }

    request_data = {
        "first_name": data.get('name'),
        "custom_fields_values": [
            {
                'field_name': 'Телефон',
                "field_code": "PHONE",
                'values': [
                    {
                        'value': data.get('phone')
                    }

                ]
            }
        ]
    }
    response = requests.post(url, json=[request_data], headers=headers)
    return response.json()

def update_deal_status(deal_data: Dict) -> Dict:
    deal = {
        'status_id': deal_data['status_id'],
        'pipeline_id': deal_data['pipeline_id']
    }

    deals_url = f'https://{settings.AMOCRM_SUBDOMAIN}.amocrm.ru/api/v4/leads/{deal_data["deal_id"]}'

    headers = {
        'Authorization': f'Bearer {settings.AMOCRM_TOKEN}',
        'Content-Type': 'application/json',
    }

    response = requests.patch(deals_url, json=deal, headers=headers)
    return response.json()

