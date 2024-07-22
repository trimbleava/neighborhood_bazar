# pages/views.py
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView


# Create your views here.
class HomePageView(TemplateView):
    # Django has a concept called the template context which means each template
    # is loaded with data from the corresponding views.py file. We can use user 
    # within template tags to access User attributes.
    template_name = "home.html"


class AboutPageView(TemplateView): 
    template_name = "about.html"
