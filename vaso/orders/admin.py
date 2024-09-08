from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import path, reverse
from orders.templatetags.admin_tags import change_status_button
from .enums import Status
from .models import Order, Payment
from .utils import get_available_statuses, update_order_status


class StatusFilter(admin.SimpleListFilter):
    title = 'Статус'
    parameter_name = 'status'

    def lookups(self, request, model_admin):
        return [(status.name, status.value) for status in Status]

    def queryset(self, request, queryset):
        if self.value():
            filtered_ids = [obj.id for obj in queryset if obj.status.name == self.value()]
            return queryset.filter(id__in=filtered_ids)
        return queryset

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):

    list_display = 'id', 'status'


@admin.register(Order)
class OrdersAdmin(admin.ModelAdmin):

    list_display = (
        'id', 'order_type', 'price', 'profile', 'city', 'address', 'courier', 'status'
    )

    list_filter = ("order_type", StatusFilter, "profile")
