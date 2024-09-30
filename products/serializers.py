from rest_framework import serializers
from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = 'id title price created'.split()
        # fields = '__all__'
        # exclude = 'price created'.split()
