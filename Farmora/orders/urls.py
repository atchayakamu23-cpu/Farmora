from django.urls import path
from . import views

urlpatterns = [
    path("cart/", views.cart, name="cart"),
    path("add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("my-orders/", views.my_orders, name="my_orders"),
    path("farmer-orders/", views.farmer_orders, name="farmer_orders"),
    path("update-status/<int:order_id>/", views.update_order_status, name="update_order_status"),
    path("<int:order_id>/", views.order_detail, name="order_detail"),
]
