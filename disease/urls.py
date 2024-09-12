from django.urls import path
from .views import check_product

urlpatterns = [
    path('', check_product, name='check_product'),
]
