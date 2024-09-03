from django.urls import path
from .views import (
    product_list, product_detail,
    collection_list, collection_detail
)

urlpatterns = [
    # Product URLs
    path('products/', product_list, name='product-list-create'),
    path('products/<int:id>/', product_detail, name='product-detail'),

    # Collection URLs
    path('collections/', collection_list, name='collection-list-create'),
    path('collections/<int:pk>/', collection_detail, name='collection-detail'),

    # As rotas para `Cart`, `Customer`, `Order`, etc. precisam ser definidas como em seu código original,
    # mas vou removê-las aqui porque elas não estão sendo mencionadas nas views atuais.
]