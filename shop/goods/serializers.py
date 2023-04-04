from rest_framework import serializers

from goods.models import Category, SubCategory, Product


class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'slug', 'image')


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'image', 'subcategories')


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('image_small', 'image_medium', 'image_large')


# class ProductSerializer(serializers.ModelSerializer):
#     subcategory = SubCategorySerializer()
#     category = CategorySerializer(source='subcategory.parent_category')
#     images = ProductImageSerializer(many=True)
#
#     class Meta:
#         model = Product
#         fields = ('id', 'name', 'slug', 'category', 'subcategory', 'images')

# class ProductSerializer(serializers.ModelSerializer):
#     subcategory = SubCategorySerializer(read_only=True)
#     category = CategorySerializer(source='subcategory.parent_category')
#     image_small = serializers.ImageField()
#     image_medium = serializers.ImageField()
#     image_large = serializers.ImageField()
#
#     class Meta:
#         model = Product
#         fields = ('name', 'slug', 'category', 'subcategory', 'price', 'image_small', 'image_medium', 'image_large')


class SimpleSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        fields = ('id', 'name', 'slug')


class SimpleCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class ProductSerializer(serializers.ModelSerializer):
    subcategory = SimpleSubCategorySerializer(read_only=True)
    category = SimpleCategorySerializer(source='subcategory.parent_category')
    image_small = serializers.ImageField()
    image_medium = serializers.ImageField()
    image_large = serializers.ImageField()

    class Meta:
        model = Product
        fields = ('name', 'slug', 'category', 'subcategory', 'price', 'image_small', 'image_medium', 'image_large')

