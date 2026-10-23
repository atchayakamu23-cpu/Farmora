from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import Profile
from .forms import ProductForm
from .models import Category, Product

def product_list(request):
    products = Product.objects.filter(available=True)
    categories = Category.objects.all()

    search = request.GET.get("search", "")
    category_id = request.GET.get("category", "")

    if search:
        products = products.filter(name__icontains=search)

    if category_id:
        products = products.filter(category_id=category_id)

    return render(
        request,
        "products/product_list.html",
        {
            "products": products,
            "categories": categories,
            "search": search,
            "selected_category": category_id,
        },
    )

def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return render(request, "products/product_detail.html", {"product": product})

def is_farmer(request):
    if not request.user.is_authenticated:
        return False
    try:
        return request.user.profile.role == "farmer"
    except Profile.DoesNotExist:
        return False

@login_required
def add_product(request):
    if not is_farmer(request):
        messages.error(request, "Only farmers can add products.")
        return redirect("product_list")

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)

        if form.is_valid():
            product = form.save(commit=False)
            product.farmer = request.user
            product.save()
            messages.success(request, "Product added successfully.")
            return redirect("my_products")
    else:
        form = ProductForm()

    return render(
        request,
        "products/product_form.html",
        {"form": form, "page_title": "Add Product"},
    )

@login_required
def my_products(request):
    if not is_farmer(request):
        return redirect("product_list")

    products = Product.objects.filter(farmer=request.user)
    return render(request, "products/my_products.html", {"products": products})

@login_required
def edit_product(request, product_id):
    if not is_farmer(request):
        return redirect("product_list")

    product = get_object_or_404(Product, id=product_id, farmer=request.user)

    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES, instance=product)

        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect("my_products")
    else:
        form = ProductForm(instance=product)

    return render(
        request,
        "products/product_form.html",
        {"form": form, "page_title": "Edit Product"},
    )

@login_required
def delete_product(request, product_id):
    if not is_farmer(request):
        return redirect("product_list")

    product = get_object_or_404(Product, id=product_id, farmer=request.user)

    if request.method == "POST":
        product.delete()
        messages.success(request, "Product deleted.")
        return redirect("my_products")

    return render(
        request,
        "products/product_confirm_delete.html",
        {"product": product},
    )
