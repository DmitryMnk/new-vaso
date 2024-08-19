from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, TemplateView

from orders.yookassa import create_payment
from .models import Bouquet, City, Colors, Package
from user.models import UserProfile
from orders.models import Order
from orders.enums import OrderType
from main.amocrm import create_deal_showcase
from datetime import timedelta
from django.utils import timezone


class BouquetDetail(DetailView):
    model = Bouquet
    template_name = 'catalog/detail.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        is_user = False
        name = ''
        phone = ''
        if self.request.user.is_authenticated:
            phone = 'есть'
            name = self.request.user.first_name
            is_user = True

        context.update({
            'phone': phone,
            'name': name,
            'is_user': is_user,
            'title': ''
        })
        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        bouquet = self.get_object()
        if bouquet.is_reserved or bouquet.is_sold:
            return redirect('main')

        is_auth = request.user.is_authenticated
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        address = request.POST.get('address')

        new_order = Order(
            order_type=OrderType.SC,
            price=bouquet.price,
            address=address,
            city=bouquet.city,
            bouquet=bouquet,
            expected_delivery_time=timezone.now() + timedelta(hours=2),
            profile=UserProfile.objects.get(user=request.user)
        )

        new_order.save()
        print(bouquet.price)
        deal_date = {
            'address': address,
            'order_id': new_order.pk,
            'price': int(bouquet.price)
        }
        bouquet.is_reserved = True
        bouquet.save()
        response = create_deal_showcase(deal_date)
        amo_id = response.get('_embedded').get('leads')[0].get('id')
        new_order.amo_id = amo_id
        new_order.save()
        payment_url = create_payment(new_order)

        return redirect(payment_url)


class CreateBouquetView(TemplateView):
    template_name = 'catalog/create_bouquet.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'colors': Colors.objects.all(),
            'package': Package.objects.all(),
            'title': ''
        })
        return context

    def post(self, request: HttpRequest) -> HttpResponse:
        data = request.POST
        print(data)
        return render(request, self.template_name, context=self.get_context_data())
