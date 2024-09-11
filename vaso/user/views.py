import random
import datetime

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from catalog.models import Bouquet
from orders.utils import create_order, create_payment
from .utils import get_or_create_user, authorize_user, send_code

from orders.models import Order
from .models import UserProfile


class UserAccountView(LoginRequiredMixin, TemplateView):
    template_name = 'user/account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = UserProfile.objects.get(user=self.request.user)
        orders = Order.objects.filter(profile=profile)
        active_orders = [order for order in orders if order.status != Order.COMPLETE]
        complete_orders = [order for order in orders if order.status == Order.COMPLETE]

        context.update({
            'orders': orders,
            'title': '',
            'active_orders': active_orders,
            'complete_orders': complete_orders,
            'points': profile.points,
            'phone': profile.phone_number
        })

        return context


class SendAuthCodeAPI(APIView):

    @staticmethod
    def post(request: Request) -> Response:
        if request.user.is_authenticated:
            return Response(status=403)

        if request.session.get('is_send'):
            send_time_str = request.session.get('send_time')
            send_time = datetime.datetime.strptime(send_time_str, '%Y-%m-%d %H:%M:%S')
            now_time = datetime.datetime.now()
            delta: datetime.timedelta = now_time - send_time
            if delta.seconds < 30:
                return Response({
                    'access': False,
                    'message': f'Сообщение можно отправить через {30 - delta.seconds} сек'
                })

        request.session['send_time'] = datetime.datetime.strftime(datetime.datetime.now(),
                                                                     '%Y-%m-%d %H:%M:%S')
        phone = request.data.get('phone')
        code = random.randint(1000, 9999)
        #send_code(phone, code)
        print(code)
        name = request.data.get('name')
        if name:
            request.session['name'] = name
        request.session['is_send'] = True
        request.session['phone'] = phone
        request.session['code'] = code

        return Response(
            {
                'message': 'Код отправлен',
                'code': code,
                'access': True
            },
            status=200
        )


class CheckCodeAPI(APIView):

    @staticmethod
    def post(request: Request) -> Response:
        if request.user.is_authenticated:
            return Response(status=403)
        code = request.session.get('code')
        user_code = request.data.get('code')
        name = request.data.get('name')
        if str(code) == user_code:
            phone = request.session['phone']
            profile = get_or_create_user(phone, name)
            authorize_user(profile, request)
            return Response({'error': False}, status=200)
        return Response({
            'error': 'Введен неверный код.'
        }, status=200)


class CheckCodeAndPayAPI(APIView):

    @staticmethod
    def post(request: Request) -> Response:
        if request.user.is_authenticated:
            return Response(status=403)
        code = request.session.get('code')
        user_code = request.data.get('code')
        name = request.data.get('name')
        address = request.data.get('address')
        b_id = request.data.get('id')
        if str(code) == user_code:
            phone = request.session['phone']
            profile = get_or_create_user(phone, name)
            bouquet = Bouquet.objects.get(pk=int(b_id))
            if bouquet.is_reserved or bouquet.is_sold:
                return Response({
                    'error': True,
                    'message': 'Букет продан'
                }, status=200)
            order_data = {
                'bouquet': bouquet,
                'city': bouquet.city,
                'profile': profile,
                'price': bouquet.price,
                'address': address,
                'name': name
            }
            bouquet.is_reserved = True
            bouquet.save()
            authorize_user(profile, request)
            new_order = create_order(True, order_data)
            payment_url = create_payment(new_order)

            return Response({'error': False, 'redirect_url': payment_url}, status=200)
        return Response({
            'error': True,
            'message': 'Введен неверный код.'
        }, status=200)


@login_required
def logout_user(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('main')
