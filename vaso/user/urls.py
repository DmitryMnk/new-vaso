from django.urls import path
from .views import UserAccountView, logout_user, SendAuthCodeAPI, CheckCodeAPI
from .utils import webhook_code

urlpatterns = [
    path('account/', UserAccountView.as_view(), name='account'),
    path('logout/', logout_user, name='logout'),
    path('webhook_code/', webhook_code, name='webhook_code'),
    path('api/send_auth_code/', SendAuthCodeAPI.as_view(), name='send_auth_code'),
    path('api/check_auth_code/', CheckCodeAPI.as_view(), name='check_auth_code'),
    path('api/check_code_and_pay/', CheckCodeAPI.as_view(), name='check_auth_code'),

]
