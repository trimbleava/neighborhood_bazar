from django.urls import path
from . import views

urlpatterns = [
    path('', views.getData),
    path ('create', views.addCustomer),
    path ('read/<str:pk>', views.getCustomer),
    path ('update/<str:pk>', views.updateCustomer),
    path ('delete/<str:pk>', views.deleteCustomer),
]