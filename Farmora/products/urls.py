from django.urls import path
from . import views

urlpatterns = [
    path("", views.product_list, name="product_list"),
    path("add/", views.add_product, name="add_product"),
    path("my-products/", views.my_products, name="my_products"),
    path("<int:product_id>/edit/", views.edit_product, name="edit_product"),
    path("<int:product_id>/delete/", views.delete_product, name="delete_product"),
    path("<int:product_id>/", views.product_detail, name="product_detail"),
]
