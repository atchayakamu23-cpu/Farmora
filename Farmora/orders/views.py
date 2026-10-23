from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import Profile
from products.models import Product
from .forms import CheckoutForm
from .models import CartItem, Order, OrderItem

def is_customer(request):
    if not request.user.is_authenticated:
        return False
    try:
        return request.user.profile.role == "customer"
    except Profile.DoesNotExist:
        return False

def is_farmer(request):
    if not request.user.is_authenticated:
        return False
    try:
        return request.user.profile.role == "farmer"
    except Profile.DoesNotExist:
        return False

@login_required
def cart(request):
    items = CartItem.objects.filter(user=request.user)
    total = Decimal("0")

    for item in items:
        total += item.total_price()

    return render(request, "orders/cart.html", {"items": items, "total": total})

@login_required
def add_to_cart(request, product_id):
    if not is_customer(request):
        messages.error(request, "Only customers can add products to cart.")
        return redirect("product_detail", product_id=product_id)

    product = get_object_or_404(Product, id=product_id, available=True)

    if product.quantity <= 0:
        messages.error(request, "Product is out of stock.")
        return redirect("product_detail", product_id=product_id)

    item = CartItem.objects.filter(
        user=request.user,
        product=product
    ).first()

    if item:
        if item.quantity < product.quantity:
            item.quantity += 1
            item.save()
    else:
        CartItem.objects.create(
            user=request.user,
            product=product,
            quantity=1
        )

    messages.success(request, "Product added to cart.")
    return redirect("cart")

@login_required
def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id, user=request.user)

    if request.method == "POST":
        item.delete()
        messages.success(request, "Item removed from cart.")

    return redirect("cart")

@login_required
def checkout(request):
    if not is_customer(request):
        return redirect("product_list")

    try:
        profile = request.user.profile
    except Profile.DoesNotExist:
        return redirect("home")

    items = CartItem.objects.filter(user=request.user)

    if not items:
        messages.info(request, "Your cart is empty.")
        return redirect("cart")

    total = Decimal("0")
    for item in items:
        if item.product.quantity < item.quantity or not item.product.available:
            messages.error(request, f"{item.product.name} is not available.")
            return redirect("cart")
        total += item.total_price()

    if request.method == "POST":
        form = CheckoutForm(request.POST)

        if form.is_valid():
            order = Order.objects.create(
                customer=request.user,
                total_amount=total,
                address=form.cleaned_data["address"],
                phone=form.cleaned_data["phone"],
            )

            for item in items:
                product = item.product

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    quantity=item.quantity,
                    price=product.price,
                )

                product.quantity -= item.quantity

                if product.quantity == 0:
                    product.available = False

                product.save()

            items.delete()

            messages.success(request, "Order placed successfully.")
            return redirect("order_detail", order_id=order.id)
    else:
        form = CheckoutForm(
            initial={
                "address": profile.address,
                "phone": profile.phone,
            }
        )

    return render(
        request,
        "orders/checkout.html",
        {"items": items, "total": total, "form": form},
    )

@login_required
def my_orders(request):
    orders = Order.objects.filter(customer=request.user)
    return render(request, "orders/my_orders.html", {"orders": orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, customer=request.user)
    return render(request, "orders/order_detail.html", {"order": order})

@login_required
def farmer_orders(request):
    if not is_farmer(request):
        return redirect("home")

    orders = Order.objects.filter(items__product__farmer=request.user).distinct()
    return render(request, "orders/farmer_orders.html", {"orders": orders})

@login_required
def update_order_status(request, order_id):
    if not is_farmer(request):
        return redirect("home")

    order = get_object_or_404(
        Order,
        id=order_id,
        items__product__farmer=request.user,
    )

    if request.method == "POST":
        status = request.POST.get("status")

        if status in dict(Order.STATUS_CHOICES):
            order.status = status
            order.save()
            messages.success(request, "Order status updated.")

    return redirect("farmer_orders")
