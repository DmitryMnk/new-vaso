from django.contrib import admin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.template.response import TemplateResponse
from django.urls import path, reverse
from orders.templatetags.admin_tags import change_status_button
from .enums import Status
from .models import Order
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


@admin.register(Order)
class OrdersAdmin(admin.ModelAdmin):

    list_display = (
        'id', 'order_type', 'price', 'profile', 'city', 'address', 'courier', 'status'
    )

    list_filter = ("order_type", StatusFilter, "profile")

    # def created_at(self, obj):
    #     for status_history_item in obj.status_history:
    #         if status_history_item.get('status') == Status.NEW:
    #             return status_history_item.get('at')
    #
    # created_at.short_description = 'Создан'
    #
    # def change_status(self, obj):
    #     available_statuses = get_available_statuses(obj.status, obj.order_type)
    #     if available_statuses:
    #         return change_status_button(obj.pk)
    #
    # change_status.short_description = 'Изменить статус'
    # change_status.allow_tags = True
    #
    # def get_urls(self):
    #     urls = super().get_urls()
    #     custom_urls = [
    #         path(
    #             'change_order_status/<uuid:order_id>/',
    #             self.admin_site.admin_view(self.change_order_status),
    #             name='change_order_status'
    #         ),
    #     ]
    #     return custom_urls + urls
    #
    # def change_order_status(self, request, order_id):
    #     order: Order = get_object_or_404(Order, pk=order_id)
    #     if request.method == 'POST':
    #         new_status = request.POST.get('status')
    #         if new_status:
    #             update_order_status(order, Status[new_status])
    #             self.message_user(request, "Статус заказа успешно изменён")
    #             return HttpResponseRedirect(reverse('admin:order_order_changelist'))
    #
    #     available_statuses = get_available_statuses(order.status, order.order_type)
    #
    #     context = {
    #         'order': order,
    #         'available_statuses': available_statuses,
    #     }
    #     return TemplateResponse(request, 'admin/order/orders/change_order_status.html', context)
