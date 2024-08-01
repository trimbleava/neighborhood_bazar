# pages/urls.py
from django.urls import path

from .views import HomePageView, AboutPageView, CopyrightPageView, OrderPageView
from pages.views import MenuListView, KitchenListView, StoreListView

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("copyright/", CopyrightPageView.as_view(), name="copyright"),
    path("about/", AboutPageView.as_view(), name="about-us"),
    path("order/", OrderPageView.as_view(), name="order-here"),
    path("menu/", MenuListView.as_view(), name="menu-list"),
    path("kitchen/", KitchenListView.as_view(), name="kitchen-list"),
    path("store/", StoreListView.as_view(), name="store-list"),
]
