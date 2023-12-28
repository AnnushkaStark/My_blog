from django.shortcuts import render
from django.views.generic.base import TemplateView
# Create your views here.

class IndexPageView(TemplateView):
    """
    Представление стратовой страницы сайта
    """
    template_name = 'index.html'