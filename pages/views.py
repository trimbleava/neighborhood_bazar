# pages/views.py
from django.utils import timezone
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic.list import ListView

from product.models import Product


class MenuListView(ListView):
    model = Product
    template_name = "menu_list.html"
    paginate_by = 5  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["today"] = timezone.now()
        return context

class KitchenListView(ListView):
    model = Product
    template_name = "kitchen_list.html"
    paginate_by = 5  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["today"] = timezone.now()
        return context

class StoreListView(ListView):
    model = Product
    template_name = "store_list.html"
    paginate_by = 5  # if pagination is desired

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["today"] = timezone.now()
        return context


# Create your views here.
class HomePageView(TemplateView):
    # Django has a concept called the template context which means each template
    # is loaded with data from the corresponding views.py file. We can use user 
    # within template tags to access User attributes.
    template_name = "home.html"


class AboutPageView(TemplateView): 
    template_name = "about.html"

    def get_context_data(self, **kwargs):
        context = super(AboutPageView, self).get_context_data(**kwargs)
        return context

class OrderPageView(TemplateView):
    template_name = "order.html"


class CopyrightPageView(TemplateView):
    template_name = "copyright.html"