"""Shopping cart functionality using session storage."""

from decimal import Decimal

from cactus_cat_software.services.models import ServicePackage


class Cart:
    """Session-based shopping cart for services."""

    def __init__(self, request):
        """Initialize the cart."""
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, service_package, quantity=1, override_quantity=False):
        """
        Add a service to the cart or update its quantity.
        """
        service_id = str(service_package.id)
        if service_id not in self.cart:
            self.cart[service_id] = {
                'quantity': 0,
                'price': str(service_package.price)
            }
        if override_quantity:
            self.cart[service_id]['quantity'] = quantity
        else:
            self.cart[service_id]['quantity'] += quantity
        self.save()

    def save(self):
        """Mark the session as modified to make sure it gets saved."""
        self.session.modified = True

    def remove(self, service_package):
        """Remove a service from the cart."""
        service_id = str(service_package.id)
        if service_id in self.cart:
            del self.cart[service_id]
            self.save()

    def __iter__(self):
        """Iterate over the items in the cart and get the services from the database."""
        service_ids = self.cart.keys()
        services = ServicePackage.objects.filter(id__in=service_ids)
        cart = self.cart.copy()
        for service in services:
            cart[str(service.id)]['service'] = service
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        """Count all items in the cart."""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        """Calculate the total price of all items in the cart."""
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """Remove cart from session."""
        del self.session['cart']
        self.save()
