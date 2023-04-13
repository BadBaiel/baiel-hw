from rest_framework import serializers
from .models import Product, Category, Review
from rest_framework.exceptions import ValidationError

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

class ProductValidateSerializers(serializers.Serializer):
    title = serializers.CharField(min_length=3, max_length=50)
    description = serializers.CharField(max_length=250, default='No description')
    price = serializers.FloatField()
    rating = serializers.FloatField(min_value=1, max_value=10)
    category_id = serializers.IntegerField()
    def create(self, validated_data):
        return Product.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.rating = validated_data.get('rating', instance.rating)
        instance.category_id = validated_data.get('category_id', instance.category_id)
        instance.save()
        return

class CategoryValidateSerializers(serializers.Serializer):
    name = serializers.CharField(min_length=3, max_length=50)

    def validate_category_id(self, category_id):
        try:
            Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            raise ValidationError(f"Error! {category_id} does not exists")
        return category_id
class ReviewValidateSerializers(serializers.Serializer):
    text = serializers.CharField(required=False)
    stars = serializers.IntegerField(min_value=1, max_value=5)
    product_id = serializers.IntegerField()
    def validate_product_id(self, product_id):
        try:
            Review.objects.get(product_id=product_id)
        except Review.DoesNotExist:
            raise ValidationError('Review doesnt exist')