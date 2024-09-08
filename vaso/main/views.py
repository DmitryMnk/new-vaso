import os

from django.db.models import Q
from django.http import FileResponse, HttpRequest, HttpResponse
from django.shortcuts import render
from django.views.generic import TemplateView
from catalog.models import Bouquet
from user.utils import get_of_create_user


class MainView(TemplateView):
    template_name = 'main/main.html'

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)
        items = Bouquet.objects.exclude(Q(bouquet_type="IB") | Q(is_sold=True) | Q(is_reserved=True))
        context.update({
            'title': '',
            'items': items,
        })
        return context


class DPInfoView(TemplateView):
    template_name = 'main/dp_info.html'


def download_file(request: HttpRequest) -> FileResponse:
    file_path = os.path.join('static/policy.pdf')  # Укажите путь к файлам
    response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
    # response['Content-Disposition'] = f'attachment; filename="policy.pdf"'
    return response


class AboutView(TemplateView):
    template_name = 'main/about.html'