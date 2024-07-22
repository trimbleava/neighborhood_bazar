from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_customers),
    path('create', views.add_customer),
    path('read/<str:pk>', views.get_customer),
    path('update/<str:pk>', views.update_customer),
    path('delete/<str:pk>', views.delete_customer),
]