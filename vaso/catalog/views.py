
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import DetailView, TemplateView
from rest_framework.exceptions import PermissionDenied
from rest_framework.views import APIView
from urllib3 import request
from rest_framework.request import Request
from rest_framework.response import Response
from orders.utils import create_order
from orders.yookassa import create_payment
from .models import Bouquet, City, Colors, Package
from user.models import UserProfile
from orders.models import Order
from orders.enums import OrderType
from main.amocrm import create_deal_showcase
from datetime import timedelta
from django.utils import timezone

from .utils import create_bouquet


class BouquetDetail(DetailView):
    model = Bouquet
    template_name = 'catalog/detail.html'
    context_object_name = 'item'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = ''
        phone = ''
        if self.request.user.is_authenticated:
            profile = UserProfile.objects.get(user=self.request.user)
            phone = profile.phone_number
            name = self.request.user.first_name

        context.update({
            'phone': phone,
            'name': name,
            'title': ''
        })
        return context

    def post(self, request: HttpRequest, *args, **kwargs) -> HttpResponse:
        if not request.user.is_authenticated:
            redirect('main')
        bouquet = self.get_object()
        if bouquet.is_reserved or bouquet.is_sold:
            return redirect('main')

        profile = UserProfile.objects.get(user=request.user)
        bouquet.is_reserved = True
        bouquet.save()

        name = request.user.first_name
        phone = request.user.username
        address = request.POST.get('address')

        order_data = {
            'bouquet': bouquet,
            'city': bouquet.city,
            'profile': profile,
            'price': bouquet.price,
            'address': address,
            'name': name
        }

        new_order = create_order(True, order_data)
        payment_url = create_payment(new_order)
        return redirect(payment_url)


class CheckFastCodeAPI(APIView):

    def post(self, request: Request) -> Response:
        if request.user.is_authenticated:
            return Response(status=403)

        user_code = request.data.get('code')
        code = request.session.get('code')
        if user_code == code:
            return Response({
                'access': True
            })
        return Response({
            'access': False
        })


class CreateBouquetView(LoginRequiredMixin, TemplateView):
    template_name = 'catalog/create_bouquet.html'
    login_url = 'main'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'colors': Colors.objects.all(),
            'package': Package.objects.all(),
            'title': ''
        })
        return context

    def post(self, request: HttpRequest) -> HttpResponse:
        profile = UserProfile.objects.get(user=request.user)
        print(request.POST)
        order_data = dict()
        order_data['colors'] = request.POST.getlist('color')
        order_data['package'] = request.POST.get('package')
        order_data['else'] = request.POST.get('else')
        order_data['address'] = request.POST.get('address')
        order_data['price'] = request.POST.get('price')
        order_data['profile'] = profile
        order_data['city'] = City.objects.get(pk=1)

        bouquet = create_bouquet({
            'price': request.POST.get('price'),
            'package': request.POST.get('package'),
        })
        order_data['bouquet'] = bouquet

        new_order = create_order(False, order_data)

        return redirect('account')
