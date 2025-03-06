from store.models import Product, Profile

class Cart():

    def __init__(self, request):
        self.session = request.session
        self.request = request
        cart = self.session.get('session_key')
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}
        self.cart = cart

    def db_add(self, product, quantity):
            product_id = str(product)
            product_qty = str(quantity)
            # Logic
            if product_id in self.cart:
                pass
            else:
                #self.cart[product_id] = {'price': str(product.price)}
                self.cart[product_id] = {'quantity': int(product_qty)}

            self.session.modified = True

            # Deal with logged in user
            if self.request.user.is_authenticated:
                # Get the current user profile
                current_user = Profile.objects.filter(user__id=self.request.user.id)
                # Convert {'3':1, '2':4} to {"3":1, "2":4}
                carty = str(self.cart)
                carty = carty.replace("\'", "\"")
                # Save carty to the Profile Model
                current_user.update(old_cart=str(carty))

    def add(self, product, quantity):

        product_id = str(product.id)
        product_qty = str(quantity)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': int(product_qty)}
        else:
            self.cart[product_id]['quantity'] += int(product_qty)
        self.session.modified = True

        # Deal with logged in user
        if self.request.user.is_authenticated:
            # Get the current user profile
            current_user = Profile.objects.filter(user__id=self.request.user.id)
			# Convert {'3':1, '2':4} to {"3":1, "2":4}
            carty = str(self.cart)
            carty = carty.replace("\'", "\"")
			# Save carty to the Profile Model
            current_user.update(old_cart=str(carty))

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

