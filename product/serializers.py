from rest_flex_fields import FlexFieldsModelSerializer
from versatileimagefield.serializers import VersatileImageFieldSerializer

from .models import Product
from .models import Image


# class ProductSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Product
#         fields = ['pk', 'name', 'category']
#         extra_kwargs = {'name': {'read_only': True}}

class ProductSerializer(FlexFieldsModelSerializer):
    class Meta:
        model = Product
        fields = ['pk', 'name', 'description', 'created', 'updated']
        expandable_fields = {
            'category': ('reviews.CategorySerializer', {'many': True}),
            'sites': ('reviews.ProductSiteSerializer', {'many': True}),
            'comments': ('reviews.CommentSerializer', {'many': True}),
            'image': ('reviews.ImageSerializer', {'many': True}),
        }


class ImageSerializer(FlexFieldsModelSerializer):
    image = VersatileImageFieldSerializer(
        sizes='product_headshot'
    )

    class Meta:
        model = Image
        fields = ['pk', 'name', 'image']