from django import template
from django.urls import reverse
from django.utils.html import format_html

register = template.Library()


@register.simple_tag
def change_status_button(order_id):
    url = reverse('admin:change_order_status', args=[order_id])
    return format_html(
        '<a class="button" href="{}">Изменить статус</a>', url
    )
