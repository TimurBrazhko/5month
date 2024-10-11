from products.models import Product
from django.http import JsonResponse
from django.forms import model_to_dict

from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from products.serializers import ProductSerializer, ProductValidateSerializer


@api_view(['GET', 'POST'])
def product_list_create_api_view(request):
    if request.method == 'GET':
        search = request.query_params.get('search', '')
        # 1 step collect data (QuerySet)
        products = (
            Product.objects.select_related('category').prefetch_related('tags', 'reviews').filter(title__icontains=search)
        )

        # step 2 reformate data(QueryDict)
        data = ProductSerializer(instance=products, many=True).data

        # step 3 return response
        return Response(data=data)

    elif request.method == 'POST':
        # step 0 validation of data(existing, typing, extra)
        serializer = ProductValidateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(status=status.HTTP_400_BAD_REQUEST,
                            data=serializer.errors)

        # 1 step: receive data from request body
        title = serializer.validated_data.get('title')
        text = serializer.validated_data.get('text')
        price = serializer.validated_data.get('price')
        is_active = serializer.validated_data.get('is_active')
        category_id = serializer.validated_data.get('category_id')
        tags = serializer.validated_data.get('tags')

        # 2 step: create product by received data
        product = Product.objects.create(
            title=title,
            text=text,
            price=price,
            is_active=is_active,
            category_id=category_id,
            # **request.data
        )
        product.tags.set(tags)
        product.save()

        # 3 step: Return response with data and status
        return Response(data={'product_id': product.id},
                        status=status.HTTP_201_CREATED)


@api_view(['GET', 'PUT', 'DELETE'])
def product_detail_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(
            status=status.HTTP_404_NOT_FOUND,
            data={"detail": "Product not found"}
        )
    if request.method == 'GET':
        data = ProductSerializer(product).data
        return Response(data=data)

    elif request.method == 'PUT':
        serializer = ProductValidateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        product.title = serializer.validated_data.get('title')
        product.text = serializer.validated_data.get('text')
        product.price = serializer.validated_data.get('price')
        product.is_active = serializer.validated_data.get('is_active')
        product.category_id = serializer.validated_data.get('category_id')
        product.tags.set(serializer.validated_data.get('tags'))
        product.save()
        return Response(data=ProductSerializer(product).data,
                        status=status.HTTP_201_CREATED)

    else:
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


def product_list_view(request):
    products = Product.objects.all()
    list_ = []
    for i in products:
        list_.append(model_to_dict(instance=i))
    return JsonResponse(list_, safe=False)
