from django.shortcuts import render, get_object_or_404, redirect
from .cart import Cart
from .forms import CartAddProduct
from online_shop.models import Product
from django.views.decorators.http import require_POST

# Create your views here.


@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProduct(request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(
            product=product, quantity=cd["quantity"], override_quantity=cd["override"]
        )

    return redirect("cart:cart_detail")


@require_POST
def cart_delete(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)

    return redirect("cart:cart_detail")


def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item["update_quantity_form"] = CartAddProduct(
            initial={"quantity": item["quantity"], "override": True}
        )
    return render(request, "cart/cart.html", {"cart": cart})
