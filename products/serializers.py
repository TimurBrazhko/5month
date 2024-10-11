from rest_framework import serializers
from products.models import Product, Category, Tag
from rest_framework.exceptions import ValidationError


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ' id name'.split()


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = 'id name'.split()


class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(many=False)
    tags = TagSerializer(many=True)
    category_name = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = 'id category category_name tags tag_list title price review_list created'.split()
        # depth = 1
        # 2 var Serializer
        # fields = '__all__'
        # exclude = 'price created'.split()

    def get_category_name(self, product):
        return product.category.name if product.category else None


class ProductValidateSerializer(serializers.Serializer):
    title = serializers.CharField(min_length=5, max_length=255)
    text = serializers.CharField(required=False, default='No text')
    price = serializers.FloatField(min_value=1, max_value=1000000)
    is_active = serializers.BooleanField(default=True)
    category_id = serializers.IntegerField()
    tags = serializers.ListField(child=serializers.IntegerField(min_value=1))

    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except:
            raise serializers.ValidationError('Category does not exist')
        return category_id

    def validate_tags(self, tags):
        tags_from_db = Tag.objects.filter(id__in=tags)  # [1, 2, 3]
        if len(tags_from_db) != len(tags):
            raise ValidationError('Tags do not exist')
        return tags


    # def validate(self, attrs):
    #     category_id = attrs['category_id']
    #     try:
    #         Category.objects.get(id=category_id)
    #     except:
    #         raise ValidationError('Category does not exist')
    #     return attrs
