from django.urls import path
from product import views

urlpatterns = [
    path('api/v1/categories/', views.categories_list_api_view),
    path('api/v1/categories/<int:id>/', views.categories_one_api_view),
    path('api/v1/product/', views.product_list_api_view),
    path('api/v1/product/<int:id>/', views.product_one_api_view),
    path('api/v1/review/', views.review_list_api_view),
    path('api/v1/review/<int:id>/', views.review_one_api_view)
]