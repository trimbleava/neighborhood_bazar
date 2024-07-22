from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from .services import Cart


class CartAPI(APIView):
    """
    Single API to handle cart operations
    """

    def get(self, request, format=None):
        cart = Cart(request)

        return Response(
            {"data": list(cart.__iter__()),
             "cart_total_price": cart.get_total_price()},
            status=status.HTTP_200_OK
        )

    def post(self, request, **kwargs):
        cart = Cart(request)

        if "remove" in request.data:
            product = request.data["product"]
            cart.remove(product)

        elif "clear" in request.data:
            cart.clear()

        else:
            product = request.data
            cart.add(
                product=product["product"],
                quantity=product["quantity"],
                overide_quantity=product["overide_quantity"] if "overide_quantity" in product else False
            )

        return Response(
            {"message": "cart updated"},
            status=status.HTTP_202_ACCEPTED)
