from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Product, Category, Review
from rest_framework import status
from .serializers import ProductSerializers, CategorySerializers, ReviewSerializers,\
    ProductValidateSerializers, CategoryValidateSerializers, ReviewValidateSerializers

                                    # """"Category"""
@api_view(['GET', 'POST'])
def categories_list_api_view(request):
    if request.method == 'GET':
        categories = Category.objects.all()
        serializer = CategorySerializers(categories, many=True)
        return Response(data=serializer.data)
    elif request.method == 'POST':
        serializers = CategoryValidateSerializers(data=request.data)
        serializers.is_valid()
        if not serializers.is_valid():
            return Response(data={'errors': serializers.errors},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        name = request.data.get('name')
        category = Category.objects.create(name=name)
        return Response(data=CategorySerializers(category).data)
@api_view(['GET', 'DELETE', 'PUT'])
def categories_one_api_view(request, id):
    try:
        category = Category.objects.get(id=id)
    except Category.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = CategorySerializers(category)
        return Response(data=serializer.data)
    elif request.method == 'DELETE':
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializers = CategoryValidateSerializers(data=request.data)
        serializers.is_valid(raise_exception=True)
        category.name = serializers.validated_data.get('name')
        return Response(data=CategorySerializers(category).data)

                                    # """Product"""
@api_view(['GET', 'POST'])
def product_list_api_view(request):
    print(request.user)
    if request.method == 'GET':
        product = Product.objects.all()
        serializer = ProductSerializers(product, many=True)
        return Response(data=serializer.data)
    elif request.method == 'POST':
        serializers = ProductValidateSerializers(data=request.data)
        serializers.is_valid()
        if not serializers.is_valid():
            return Response(data={'errors': serializers.errors},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        title = serializers.validated_data.get('title')
        description = serializers.validated_data.get('description')
        price = serializers.validated_data.get('price')
        rating = serializers.validated_data.get('rating')
        category = serializers.validated_data.get('category')
        product = serializers.validated_data.create(title=title, description=description,
                                         price=price, rating=rating, category=category)
        return Response(data=ProductSerializers(product).data)
@api_view(['GET', 'DELETE', 'PUT'])
def product_one_api_view(request, id):
    try:
        product = Product.objects.get(id=id)
    except Product.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ProductSerializers(product)
        return Response(data=serializer.data)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializers = ProductValidateSerializers(data=request.data)
        serializers.is_valid(raise_exception=True)
        product.title = serializers.validated_data.get('title')
        product.description = serializers.validated_data.get('description')
        product.price = serializers.validated_data.get('price')
        product.rating = serializers.validated_data.get('rating')
        product.category = serializers.validated_data.get('category')
        product.save()
        return Response(data=ProductSerializers(product).data)

                                   # """Review"""
@api_view(['GET', 'POST'])
def review_list_api_view(request):
    if request.method == 'GET':
        review = Review.objects.all()
        serializer = ReviewSerializers(review, many=True)
        return Response(data=serializer.data)
    elif request.method == 'POST':
        serializers = ReviewValidateSerializers(data=request.data)
        serializers.is_valid()
        if not serializers.is_valid():
            return Response(data={'errors': serializers.errors},
                            status=status.HTTP_406_NOT_ACCEPTABLE)
        text = request.data.get('text')
        product_id = request.data.get('product_id')
        stars = request.data.get('stars')
        review = Review.objects.create(text=text, product_id=product_id, stars=stars)
        return Response(data=ReviewSerializers(review).data)


@api_view(['GET', 'DELETE', 'PUT'])
def review_one_api_view(request, id):
    try:
        review = Review.objects.get(id=id)
    except Review.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    if request.method == 'GET':
        serializer = ReviewSerializers(review)
        return Response(data=serializer.data)
    elif request.method == 'DELETE':
        review.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    elif request.method == 'PUT':
        serializers = ReviewValidateSerializers(data=request.data)
        serializers.is_valid(raise_exception=True)
        review.name = serializers.validated_data.get('name')
        return Response(data=ReviewSerializers(review).data)
