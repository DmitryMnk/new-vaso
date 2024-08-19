from typing import Dict

from vaso import settings
import requests

PIPELINES = {
    'Идеальный букет': {
        'id': 8385254,
        'statuses': {
            'Анкета заполнена': 68290058,
            'Букет собран': 68290062,
            'Принимают решение': 68290066,
            'Букет на доработке': 68290070,
            'Оплачивают': 68705866,
            'Оплачен': 68705870,
            'Поиск курьера': 68705874,
            'Передан курьеру': 68705878,
            'Доставлено': '68705882'
        }
    },
    'Витрина': {
        'id': 8415638,
        'statuses': {
            'Оплачивают': 68707870,
            'Оплачен': 68497838,
            'Поиск курьера': 68497842,
            'Передан курьеру': 68497846,
            'Доставлено': '68706158'
        },
        'fields': {
            'Адрес': 898593,
            'Имя': 901495,
            'Телефон': 901497,
            'order_id': 901501,
            'Дата': 898595
        }

    },
    'Мессенджеры': 8415650
}


def create_deal_showcase(deal_data: Dict):
    deal = {
        "name": "Название сделки",  # Название сделки
        "price": deal_data.get('price'),  # Сумма сделки
        "pipeline_id": PIPELINES['Витрина']['id'],  # ID воронки, в которую добавляется сделка
        "status_id": PIPELINES['Витрина']['statuses']['Оплачивают'],  # ID статуса сделки в воронке
        "custom_fields_values": [
            {
                'field_id': PIPELINES['Витрина']['fields']['Адрес'],
                "values": [
                    {
                        'enum_id': 1,
                        'value': deal_data.get('address')
                    }
                ]
            },
            {
                'field_id': PIPELINES['Витрина']['fields']['order_id'],
                "values": [
                    {
                        'value': deal_data.get('order_id')
                    }
                ]
            },
        ]
    }

    deals_url = f'https://{settings.AMOCRM_SUBDOMAIN}.amocrm.ru/api/v4/leads'
    headers = {
        'Authorization': f'Bearer {settings.AMOCRM_TOKEN}',
        'Content-Type': 'application/json',
    }

    response = requests.post(deals_url, json=[deal], headers=headers)
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
    print(response.json())
    return response.json()
