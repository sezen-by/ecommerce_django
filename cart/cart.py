from store.models import Product

class Cart():
	def __init__(self, request):
		self.session = request.session
		# Get request
		self.request = request
		# Get the current session key if it exists
		cart = self.session.get('session_key')

		# If the user is new, no session key!  Create one!
		if 'session_key' not in request.session:
			cart = self.session['session_key'] = {}


		# Make sure cart is available on all pages of site
		self.cart = cart


	def add(self, product):
		# Get product id
		product_id = str(product.id)

		# If product is not in cart, add it
		if product_id not in self.cart:
			self.cart[product_id] = {'price': str(product.price)}

		# Save
		self.session.modified = True

	def __len__(self):
		return len(self.cart)

	def get_prods(self):
		# Get ids from carts
		product_ids = self.cart.keys()
		# Use ids to lookup products in database model
		products = Product.objects.filter(id__in=product_ids)
		# Return those looked up products
		return products
