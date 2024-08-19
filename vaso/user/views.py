import random

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect
from django.views.generic import TemplateView
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from orders.models import Order
from .models import UserProfile


class UserAccountView(LoginRequiredMixin, TemplateView):
    template_name = 'user/account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile = UserProfile.objects.get(user=self.request.user)
        orders = Order.objects.filter(profile=profile)
        context.update({
            'orders': orders,
            'title': ''
        })

        return context


def send_auth_code(self, request: Request, phone: str) -> Response:
    if request.user.is_authenticated:
        return Response(status=403)

    code = random.randint(1000, 9999)
    request.session['code'] = code
    print(code)
    return Response({'message': 'Код отправлен'}, status=200)


@login_required
def logout_user(request: HttpRequest) -> HttpResponse:
    logout(request)
    return redirect('main')
