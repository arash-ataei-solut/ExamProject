from rest_framework import serializers

from .models import Product, Subcategory, Category, MediaFile, Rate
from store.serializers import StoreSerializer
from user.serializers import ProfileSerializer


class SubcategorySerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Subcategory
        fields = ['url', 'id', 'name', 'num_chasers']


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    subcategories = SubcategorySerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['url', 'id', 'name', 'num_chasers', 'subcategories']


class SubcategoryDetailSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    chasers = ProfileSerializer(many=True)

    class Meta:
        model = Subcategory
        fields = ['name', 'id', 'category', 'chasers', 'num_chasers']


class CategoryDetailSerializer(serializers.ModelSerializer):
    chasers = ProfileSerializer(many=True)

    class Meta:
        model = Category
        fields = ['name', 'id', 'chasers', 'num_chasers']


class HideMediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = MediaFile
        fields = ['id', 'price', 'file_size']


class MediaSerializer(serializers.ModelSerializer):

    class Meta:
        model = MediaFile
        fields = ['id', 'file_size', 'file']


class ProductSerializer(serializers.HyperlinkedModelSerializer):
    sender = ProfileSerializer(read_only=True)

    class Meta:
        model = Product
        fields = ['url', 'id', 'sender', 'title', 'cover']


class ProductDetailSerializer(serializers.ModelSerializer):
    store = StoreSerializer()
    sender = ProfileSerializer(read_only=True)
    subcategories = SubcategorySerializer(many=True)
    viewed_by = ProfileSerializer(many=True)
    views = serializers.SerializerMethodField()

    def get_views(self, product):
        return product.viewed_by.all().count()

    class Meta:
        model = Product
        fields = [
            'id',
            'store',
            'sender',
            'title',
            'caption',
            'subcategories',
            'viewed_by',
            'views',
            'is_special',
            'price',
        ]


class RateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rate
        fields = ['rate']
