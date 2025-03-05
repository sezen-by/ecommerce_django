from store.models import Product

class Cart():

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('session_key')
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        self.cart = cart

    def add(self, product, quantity):

        product_id = str(product.id)
        product_qty = str(quantity)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': int(product_qty)}
        else:
            self.cart[product_id]['quantity'] += int(product_qty)
        self.session.modified = True

    def __len__(self):

        return sum(item['quantity'] if isinstance(item, dict) else 0 for item in self.cart.values())

    def cart_total(self):

        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        quantities = self.cart
        total = 0
        for key, value in quantities.items():
            for product in products:
                if str(product.id) == key:
                    if product.is_sale:
                        total += (product.sale_price * value["quantity"])
                    else:
                        total += (product.price * value["quantity"])
        return total


    def get_prods(self):

        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        return products
    
    def get_quants(self):

        quantities = self.cart
        return quantities
        
    def update(self, product, quantity):

        product_id = str(product.id)
        product_qty = int(quantity)
        if product_id in self.cart:
            self.cart[product_id]['quantity'] = product_qty
        else:
            # Eğer ürün sepette mevcut değilse, yeni bir ürün ekle
            self.cart[product_id] = {'quantity': product_qty}
        self.session.modified = True  # Seansı değiştir
        

    def delete(self, product):

        product_id = str(product)
            # Delete from dictionary/cart
        if product_id in self.cart:
            del self.cart[product_id]
        self.session.modified = True

