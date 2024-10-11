from django.contrib import admin
from products.models import Product, Category, Tag, Review


class ReviewInline(admin.StackedInline):
    model = Review
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    inlines = [ReviewInline]


admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Tag)
