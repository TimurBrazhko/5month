from products.models import Product
from django.http import JsonResponse
from django.forms import model_to_dict

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from products.serializers import ProductSerializer


@api_view(['GET'])
def product_list_api_view(request):
    # 1 step collect data (QuerySet)
    products = Product.objects.all()

    # step 2 reformate data(QueryDict)
    data = ProductSerializer(instance=products, many=True).data

    # step 3 return response
    return Response(data=data)


@api_view(['GET'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(
            status=status.HTTP_404_NOT_FOUND,
            data={"detail": "Product not found"}
        )
    data = ProductSerializer(product).data
    return Response(data=data)


def product_list_view(request):
    products = Product.objects.all()
    list_ = []
    for i in products:
        list_.append(model_to_dict(instance=i))
    return JsonResponse(list_, safe=False)
