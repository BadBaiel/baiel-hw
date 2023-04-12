from rest_framework import serializers
from .models import Product, Category, Review


class CategorySerializers(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = 'id name products_count products_list'.split()

class ReviewSerializers(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = 'id text product stars'.split()

class ProductSerializers(serializers.ModelSerializer):
    review = ReviewSerializers(many=True)

    class Meta:
        model = Product
        fields = 'id title description price category review'.split()

    def get_review(self, product):
        return product.review

class RatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = 'title rating'.split()