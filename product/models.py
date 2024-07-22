from django.db import models
from versatileimagefield.fields import VersatileImageField, PPOIField


class Company(models.Model):
    # https://medium.com/django-rest/lets-build-a-basic-product-review-backend-with-drf-part-1-652dd9b95485
    name = models.CharField(max_length=255)
    url = models.TextField()

    def __str__(self):
        return self.name


class ProductSize(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.ManyToManyField(Category, related_name='products')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ManyToManyField('Image', related_name='products', blank=True)  # upload_to='products/%Y/%m/%d',
    is_available = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name


class ProductSite(models.Model):
    name = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='sites', related_query_name='site')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='sites', related_query_name='site')
    productsize = models.ForeignKey(ProductSize, on_delete=models.CASCADE, related_name='sites', related_query_name='site')
    price = models.DecimalField(max_digits=9, decimal_places=2)
    url = models.TextField()
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class Image(models.Model):
    name = models.CharField(max_length=255)
    image = VersatileImageField(
        'Image',
        upload_to='images/',
        ppoi_field='image_ppoi'
    )
    image_ppoi = PPOIField()

    def __str__(self):
        return self.name
