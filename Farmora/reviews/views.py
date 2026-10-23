from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import Profile
from products.models import Product
from .forms import ReviewForm
from .models import Review

@login_required
def add_review(request, product_id):
    product = get_object_or_404(Product, id=product_id)

    try:
        if request.user.profile.role != "customer":
            return redirect("product_detail", product_id=product.id)
    except Profile.DoesNotExist:
        return redirect("product_detail", product_id=product.id)

    old_review = Review.objects.filter(
        product=product,
        user=request.user
    ).first()

    if request.method == "POST":
        form = ReviewForm(request.POST, instance=old_review)

        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()

            messages.success(request, "Review saved.")
            return redirect("product_detail", product_id=product.id)
    else:
        form = ReviewForm(instance=old_review)

    return render(
        request,
        "reviews/review_form.html",
        {"form": form, "product": product},
    )

@login_required
def delete_review(request, review_id):
    review = get_object_or_404(Review, id=review_id, user=request.user)
    product_id = review.product.id

    if request.method == "POST":
        review.delete()
        messages.success(request, "Review deleted.")

    return redirect("product_detail", product_id=product_id)
