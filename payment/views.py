from django.shortcuts import render
from cart.cart import Cart
from payment.forms import ShippingForm
from payment.models import ShippingAddress
# Create your views here.


def checkout(request): 
    # Get the cart
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    if request.user.is_authenticated:
        # Shipping User
        shipping_user = ShippingAddress.objects.filter(user__id=request.user.id).first()

        if not shipping_user:
            shipping_user = ShippingAddress(user=request.user)  # Yeni bir ShippingAddress nesnesi oluştur
            shipping_user.save()  # Kaydedin, böylece veri tabanında yer alsın

        # Shipping Form
        shipping_form = ShippingForm(request.POST or None, instance=shipping_user)

        return render(request, "payment/checkout.html", {
            "cart_products": cart_products,
            "quantities": quantities,
            "totals": totals,
            "shipping_form": shipping_form
        })
    
    else:
        # Checkout as guest
        shipping_form = ShippingForm(request.POST or None)
        return render(request, "payment/checkout.html", {
            "cart_products": cart_products,
            "quantities": quantities,
            "totals": totals,
            "shipping_form": shipping_form
        })

	


def payment_success(request):
    return render(request, "payment/payment_success.html", {} )
