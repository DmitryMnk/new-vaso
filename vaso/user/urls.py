from django.urls import path
from .views import UserAccountView, logout_user, send_auth_code

urlpatterns = [
    path('account/', UserAccountView.as_view(), name='account'),
    path('logout/', logout_user, name='logout'),
    path('api/send_auth_code/', send_auth_code, name='send_auth_code'),
]
