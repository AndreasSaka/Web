import json
from django.contrib.auth import logout
from .models import Customer, ProductCategory, Product, Order, OrderItem, ShippingAddress


def cookieCart(request):
    """ This function makes a dictionary represantation of an order. That is because a guest never actually creates an order until checkout. Everything is stored in cookies. """
    try:
        # Retrieve and parse cookie 'cart'.
        cart = json.loads(request.COOKIES['cart'])
    except:
        # Creating a cart cookie for first time visitors.
        cart = {}
        print('CART:', cart)
    # Rersesents an empty cart for non-logged in user.
    items = [] 
    order = { 'get_cart_total': 0, 'get_cart_items': 0 }
    cartItems = order['get_cart_items']
    # Cart looks like this : cart = { '1': {'quantity': 3}, '2': {'quantity': 5} }
    for i in cart:
        try:
            cartItems += cart[i]['quantity']
            product = Product.objects.get(id=i)
            total = (product.price * cart[i]['quantity'])
            order['get_cart_total'] += total
            order['get_cart_items'] += cart[i]['quantity']
            # Represents the product that will be ordered.
            item = {
                'id': product.id,
                'product': {
                    'id': product.id,
                    'name': product.name, 
                    'price': product.price, 
                    'imageURL': product.imageURL,
                }, 

                'quantity': cart[i]['quantity'],
                'get_total': total,
            }
            # Adding product to the cart.
            items.append(item)
        except:
            pass
    return {'items': items, 'order': order, 'cartItems': cartItems}


def cartData(request):
    """ Checks whether the user is authenticated or not. Then returns a dictionary with information, in order to be rendered in views.py """
    isguest = None
    isloginuser = None

    """In case of guest create a cart in cookies"""
    """In case of authenticated user bring the stored cart or create a new one"""
    if request.user.is_anonymous:
        print("222222")
        isguest= True
        cookieData = cookieCart(request)
        # cartItems refers to the cart navbar icon.
        cartItems = cookieData['cartItems']
        order = cookieData['order']
        items = cookieData['items']    
    elif request.user.is_authenticated:
        print("11111111")
        isloginuser = True
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        # cartItems refers to the cart navbar icon.
        cartItems = order.get_cart_items

        # This check is done so the superuser can only be logged in the admin site
        if request.user.is_superuser:
            isloginuser = False
            logout(request)
            isguest = True
    return {'cartItems': cartItems , 'order': order, 'items': items, 'isguest': isguest, 'isloginuser': isloginuser}


def guestOrder(request, data):
    """ Creates an order for the guest and returns it. """
    first_name = data['form']['first_name']
    last_name = data['form']['last_name']
    email = data['form']['email']

    cookieData = cookieCart(request)
    items = cookieData['items']

    customer, created = Customer.objects.get_or_create(email=email,)
    customer.first_name = first_name
    customer.last_name = last_name
    customer.save()
    order = Order.objects.create(customer=customer, complete=False,)

    for item in items:
	    product = Product.objects.get(id=item['id'])
	    orderItem = OrderItem.objects.create(
		    product=product,
			order=order,
			quantity=item['quantity'],
		)
    return customer, order

def adminCheck(request):
    """ Check if admin/superuser and force to logout """
    if request.user.is_authenticated and request.user.is_superuser:
      logout(request)