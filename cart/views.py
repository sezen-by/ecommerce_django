from django.shortcuts import render, get_object_or_404
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages
from .cart import Cart

def cart_summary(request):
	# Get the cart
	cart = Cart(request)
	# Get the products
	cart_products = cart.get_prods()
	return render(request, 'cart_summary.html', {"cart_products": cart_products})

def cart_add(request):
	# Get the cart
	cart = Cart(request)
	# test for POST
	if request.POST.get('action') == 'post':
		# Get stuff
		product_id = int(request.POST.get('product_id'))

		# lookup product in DB
		product = get_object_or_404(Product, id=product_id)
		
		# Save to session
		cart.add(product=product)

		# Get Cart Quantity
		cart_quantity = cart.__len__()
        
		# Return resonse
		# response = JsonResponse({'Product Name: ': product.name})
		print(f"✅ Sepetteki toplam ürün: {cart_quantity}")
		response = JsonResponse({'qty': cart_quantity})
		messages.success(request, ("Product Added To Cart..."))
		return response
