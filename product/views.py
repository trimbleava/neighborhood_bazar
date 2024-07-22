from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ReadOnlyModelViewSet
from rest_flex_fields.views import FlexFieldsModelViewSet
from rest_framework.permissions import IsAuthenticated

from .serializers import ProductSerializer
from .serializers import ImageSerializer
from .models import Product
from .models import Image


class ProductViewSet(ReadOnlyModelViewSet):

    serializer_class = ProductSerializer
    queryset = Product.objects.all()


class ImageViewSet(FlexFieldsModelViewSet):

    serializer_class = ImageSerializer
    queryset = Image.objects.all()
    permission_classes = [IsAuthenticated]


class ProductAPI(APIView):
    """
    Single API to handle product operations
    """
    serializer_class = ProductSerializer

    # def get(self, request, format=None):
    #     qs = Product.objects.all()
    #
    #     return Response(
    #         {"data": self.serializer_class(qs, many=True).data},
    #         status=status.HTTP_200_OK
    #     )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

