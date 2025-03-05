from pyexpat.errors import messages
from django.shortcuts import render, get_object_or_404
from store.models import Product
from django.http import JsonResponse
from .cart import Cart
from django.contrib import messages

def cart_summary(request):
    
    cart = Cart(request)
    cart_products = cart.get_prods()
    quantities = cart.get_quants()
    totals = cart.cart_total()
    return render(request, 'cart_summary.html', {"cart_products": cart_products, "quantities": quantities, "totals": totals})


def cart_add(request):
    
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty', 1))  # Varsayılan olarak 1
        product = get_object_or_404(Product, id=product_id) #Product modelinden product_id ile ilgili ürün alınır.
        cart.add(product=product, quantity=product_qty)
        cart_quantity = cart.__len__()
        response = JsonResponse({'qty': cart_quantity})
        messages.success(request, ("Product Added to Cart"))
        return response
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)


def cart_update(request):
    
    cart = Cart(request)
    # Eğer POST verisi 'action' değeri 'post' değilse, bir hata döndür
    if request.POST.get('action') != 'post':
        return JsonResponse({'error': 'Invalid request'}, status=400)
    # POST verisi geçerli, ürün ID'sini ve yeni miktarını al
    product_id = int(request.POST.get('product_id'))
    product_qty = int(request.POST.get('product_qty'))
    # Ürünü almak için `get_object_or_404` fonksiyonunu kullanıyoruz
    product = get_object_or_404(Product, id=product_id)
    print(product)
    # Sepeti güncelleme işlemi
    cart.update(product=product, quantity=product_qty)
    # Güncellenmiş sepetin toplam miktarını alıyoruz
    cart_quantity = cart.__len__()
    print(cart_quantity)
    # JsonResponse döndürerek güncellenmiş miktarı döndürüyoruz
    messages.success(request, ("Your cart has been updated"))
    return JsonResponse({'qty': cart_quantity})


def cart_delete(request):
    
    cart = Cart(request)
    if request.POST.get('action') == 'post':
        # Get stuff
        product_id = int(request.POST.get('product_id'))
        # Call delete Function in Cart
        cart.delete(product=product_id)
        response = JsonResponse({'product':product_id})
        #return redirect('cart_summary')
        messages.success(request, ("Item Deleted From Shopping Cart"))
        return response 

