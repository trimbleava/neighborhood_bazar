from django.contrib import admin

from .models import Product
from .models import Image


admin.site.register(Product)
admin.site.register(Image)