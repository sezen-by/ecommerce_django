from django.shortcuts import render, get_object_or_404
#from .cart import Cart
from store.models import Product
from django.http import JsonResponse
from django.contrib import messages

def cart_summary(request):
    return render(request, 'cart_summary.html')