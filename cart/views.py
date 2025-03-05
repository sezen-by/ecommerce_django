from pyexpat.errors import messages
from django.shortcuts import render, get_object_or_404
from store.models import Product
from django.http import JsonResponse
from .cart import Cart

def cart_summary(request):
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    return render(request, 'cart_summary.html', {"cart_products": cart_products, "quantities": quantities})

def cart_add(request):
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty', 1))  # Varsayılan olarak 1
        product = get_object_or_404(Product, id=product_id) #Product modelinden product_id ile ilgili ürün alınır.
        cart.add(product=product, quantity=product_qty)
        cart_quantity = cart.__len__()
        response = JsonResponse({'qty': cart_quantity})
        return response
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)

def cart_update(request):
	cart = Cart(request)
	if request.POST.get('action') == 'post':
		# Get stuff
		product_id = int(request.POST.get('product_id'))
		product_qty = int(request.POST.get('product_qty'))

		cart.update(product=product_id, quantity=product_qty)

		response = JsonResponse({'qty':product_qty})
		#return redirect('cart_summary')

		return response
    
def cart_delete(request):
    pass
	# cart = Cart(request)
	# if request.POST.get('action') == 'post':
	# 	# Get stuff
	# 	product_id = int(request.POST.get('product_id'))
	# 	# Call delete Function in Cart
	# 	cart.delete(product=product_id)

	# 	response = JsonResponse({'product':product_id})
	# 	#return redirect('cart_summary')
	# 	messages.success(request, ("Item Deleted From Shopping Cart..."))
	# 	return response 

