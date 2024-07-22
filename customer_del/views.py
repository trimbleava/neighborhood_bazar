from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import Customer
from .serializers import CustomerSerializer


@api_view(['GET'])
def get_customers(request):
    customers = Customer.objects.all()
    serializer = CustomerSerializer(customers, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def get_customer(request, pk):
    customers = Customer.objects.get(id=pk)
    serializer = CustomerSerializer(customers, many=False)
    return Response(serializer.data)


@api_view(['POST'])
def add_customer(request):
    serializer = CustomerSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['PUT'])
def update_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    serializer = CustomerSerializer(instance=customer, data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(serializer.data)


@api_view(['DELETE'])
def delete_customer(request, pk):
    customer = Customer.objects.get(id=pk)
    customer.delete()
    return Response('Customer successfully deleted!')

