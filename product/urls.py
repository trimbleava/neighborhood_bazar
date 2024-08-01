# product/urls.py
from django.urls import path

from .views import ProductPageView

urlpatterns = [
    path("", ProductPageView.as_view(), name="home"),
]