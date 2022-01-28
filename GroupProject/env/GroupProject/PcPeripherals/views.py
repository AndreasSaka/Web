''' Coding Bootcamp 
-Title:  GroupProject 
-Last name : Pantelakis
-First Name: Ioannis
-Team: Dikas Giorgos - Nikolaou Ioannis - Patralis Athanasios - Pantelakis Ioannis - Sakapetis Andreas
-Advisors: Tyrovola Sarantia, Nikolaos Avgeros
-Python ver:3.9.2
-win: win10 64bit
'''

import json
from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.http.response import HttpResponseRedirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .forms import CustomerRegistrationForm, LoginForm, CustomerForm
from .utils import cookieCart, cartData, guestOrder, adminCheck
from .models import Customer, ProductCategory, Product, Order, OrderItem, ShippingAddress
from .models import *
from .utils import cookieCart, cartData, guestOrder
from rest_framework import viewsets
from .serializers import CustomerSerializer, ProductCategorySerializer, ProductSerializer, OrderSerializer
import json
from django.contrib.auth.decorators import login_required

# Home Page
def home_page(request):
    adminCheck(request)
    products = Product.objects.all()
    context = {}
    data = cartData(request)

    #Creating pagination 
    page = request.GET.get('page', 1)
    paginator = Paginator(products, 9)
    try:
        product_lists = paginator.page(page)
    except PageNotAnInteger:
        product_lists = paginator.page(1)
    except EmptyPage:
        product_lists = paginator.page(paginator.num_pages)

    username = request.user.username
    context['username'] = username
    context['isguest'] = data['isguest']
    context['isloginuser'] = data['isloginuser']
    context['items'] = data['items']
    context['cartItems'] = data['cartItems'] 
    context['order'] = data['order']
    context['request'] = request
    context['product_lists'] = product_lists
    return render(request, 'PcPeripherals/home.html', context)


# About Page
def about_page(request):
    adminCheck(request)
    context = {}
    data = cartData(request)
    username = request.user.username
    context['username'] = username
    context['isguest'] = data['isguest']
    context['isloginuser'] = data['isloginuser']
    context['cartItems'] = data['cartItems']
    context['items'] = data['items']
    context['order'] = data['order']
    return render(request, 'PcPeripherals/about.html', context)


# Contact Page
def contact_page(request):
    adminCheck(request)
    context={}
    data = cartData(request)
    username = request.user.username
    context['username'] = username
    context['isguest'] = data['isguest']
    context['isloginuser'] = data['isloginuser']
    context['items'] = data['items']
    context['cartItems'] = data['cartItems'] 
    context['order'] = data['order']
    return render(request, 'PcPeripherals/contact.html', context)


# User Registration
def customer_registration(request):
    adminCheck(request)
    context={}
    if request.method == 'POST':
        customer_form = CustomerRegistrationForm(request.POST)
        if customer_form.is_valid():
            customer_form.save()

            username = customer_form.cleaned_data.get('username')
            password = customer_form.cleaned_data.get('password1')
            firstname = customer_form.cleaned_data.get('first_name') 
            lastname = customer_form.cleaned_data.get('last_name')
            email = customer_form.cleaned_data.get('email')
            user = User.objects.get(username=username) 

            # creating user record on models
            customer = Customer(user=user, first_name=firstname, last_name=lastname, email=email)
            customer.save()

            user = authenticate(request, username=username, password=password) 
            login(request, user)
            return HttpResponseRedirect('/pcp/home/')
    else:
        customer_form = CustomerRegistrationForm()
    data = cartData(request) # function in utils.py

    context['isguest'] = data['isguest']
    context['isloginuser'] = data['isloginuser']
    context['items'] = data['items']
    context['cartItems'] =  data['cartItems']  
    context['form'] = customer_form
    context['order'] = data['order']
    return render(request, 'PcPeripherals/user_registration.html', context)


# User Login
def user_login(request):
    adminCheck(request) 
    context = {}
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                if request.user.is_superuser:  #Redirect admin users on admin site
                    logout(request)
                    return HttpResponseRedirect('http://localhost:8000/admin/')
                else:
                    return HttpResponseRedirect('/pcp/home/') 
            else:
                if not username:
                    context['empty_username'] = 'Please enter a username'
                elif not password:
                    context['empty_password'] = 'Please enter a password'
                elif user is None:
                    context['invalid'] = 'Username and password do not match'
    else:
        login_form = LoginForm()

    data = cartData(request) # function in utils.py  
    context['isguest'] = data['isguest']
    context['isloginuser'] = data['isloginuser']
    context['items'] = data['items']
    context['cartItems'] =  data['cartItems']  
    context['form'] = login_form
    context['order'] = data['order']
    return render(request, 'PcPeripherals/user_login.html', context)


# User Profile
def user_profile(request):
    adminCheck(request)
    context = {}
    customer = request.user.customer
    form = CustomerForm(instance=customer)
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()

    data = cartData(request)
    username = request.user.username
    context['username'] = username
    context['isguest'] = data['isguest']
    context['isloginuser'] = data['isloginuser']
    context['items'] = data['items']
    context['cartItems'] = data['cartItems'] 
    context['order'] = data['order']
    context['form'] = form
    return render(request, 'PcPeripherals/profile.html', context)


# User Logout
def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/pcp/login/')


# Category (Monitor, Mouse, Keyboard)
def monitor(request):
    adminCheck(request)
    monitors = Product.objects.filter(category=1)
    context = {}
    data = cartData(request)
    username = request.user.username
    context['username'] = username
    context['monitors'] = monitors
    context['isguest'] = data['isguest']
    context['isloginuser'] = data['isloginuser']
    context['items'] = data['items']
    context['cartItems'] = data['cartItems']
    context['order'] = data['order']
    return render(request, 'PcPeripherals/monitor.html', context)


def mouse(request):
    adminCheck(request)
    mouses = Product.objects.filter(category=2)
    context = {}
    data = cartData(request)
    username = request.user.username
    context['username'] = username
    context['mouses'] = mouses
    context['isguest'] = data['isguest']
    context['isloginuser'] = data['isloginuser']
    context['items'] = data['items']
    context['cartItems'] = data['cartItems']
    context['order'] = data['order']
    return render(request, 'PcPeripherals/mouse.html', context)


def keyboard(request):
    adminCheck(request)
    keyboards = Product.objects.filter(category=3)
    context = {}
    data = cartData(request)
    username = request.user.username
    context['username'] = username
    context['keyboards'] = keyboards
    context['isguest'] = data['isguest']
    context['isloginuser'] = data['isloginuser']
    context['items'] = data['items']
    context['cartItems'] = data['cartItems']
    context['order'] = data['order']
    return render(request, 'PcPeripherals/keyboard.html', context)


# Checkout
def checkout(request):
    adminCheck(request)
    context = {}
    data = cartData(request)
    context['isguest'] = data['isguest']
    context['isloginuser'] = data['isloginuser']
    context['cartItems'] = data['cartItems']
    context['items'] = data['items']
    context['order'] = data['order']
    return render(request, 'PcPeripherals/checkout.html', context)
   

# Cart
def cart(request):
    adminCheck(request)
    context = {}
    data = cartData(request)
    context['isguest'] = data['isguest']
    context['isloginuser'] = data['isloginuser']
    context['cartItems'] = data['cartItems']
    context['items'] = data['items']
    context['order'] = data['order']
    return render(request, 'PcPeripherals/cart.html', context)


# Update Item
def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
    # Checking tests
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)

     # Use get_or_create because we want to have the ability to update the quantity of an order in the cart page, instead of creating a new one.
	order, created = Order.objects.get_or_create(customer=customer, complete=False)
	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    # Refers to buttons' action attributes.
	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)
	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()
	return JsonResponse('Item was added', safe=False)


# Process Order
def processOrder(request):
    transaction_id = datetime.now().timestamp()
    # Parse the data.
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()
    
    ShippingAddress.objects.create(
        customer=customer,
        order=order,
        address=data['shipping']['address'],
        city=data['shipping']['city'],
        state=data['shipping']['state'],
        zipcode=data['shipping']['zipcode'],
    )
    return JsonResponse('Payment submitted..', safe=False)

#Serializers-Api views

class CustomerView(viewsets.ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer

class ProductCategoryView(viewsets.ModelViewSet):
    queryset = ProductCategory.objects.all()
    serializer_class = ProductCategory

class ProductView(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

class OrderView(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

import os
import requests

os.environ['NO_PROXY'] = '127.0.0.1'
def api_view1(request):  #View presenting apis results-only admin permission
    is_admin = request.user.is_superuser
    if  is_admin:
        #url = 'http://127.0.0.1:8000/pcp/customer/'
        #url = 'http://127.0.0.1:8000/pcp/customer/?format=api'
        url = 'http://127.0.0.1:8000/pcp/customer/?format=json'
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'Referer': 'http://localhost:8000/pcp/customer/',
            'Connection': 'keep-alive',
            'Cookie': 'N7jxVi2WAtt90DtOBidsCugei4DsHiYsHd7LneYXWQauMsYuvfc7HDhmaQiY6zjq; sessionid=hf20vqqh19nqaquukem61wqq5sor4tss'}
        r = requests.get(url,headers=headers)
        data = json.loads(r.text)
        return render(request,'PcPeripherals/api.html',{'response':data, 'request':request})
    else:
        return HttpResponseRedirect('/pcp/home/')   







def login_api(request): #  #login for api_view only admin permission
    
    logout(request)
    context = {}

    if request.method == 'POST':
        
        login_form2 = LoginForm(request.POST)
        if login_form2.is_valid():
            username = login_form2.cleaned_data.get('username')
            password = login_form2.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)
            login(request, user)
            is_admin = request.user.is_superuser
            if user is not None and is_admin:
                return HttpResponseRedirect('/pcp/api/')
            elif user.is_authenticated and not is_admin:
                return HttpResponseRedirect('/pcp/home/')
            else:
                if not username:
                    context['empty_username'] = 'Please enter a username'
                elif not password:
                    context['empty_password'] = 'Please enter a password'
                elif user is None:
                    context['invalid'] = 'Username and password do not match'
    else:
        login_form2 = LoginForm()

    return render(request, 'PcPeripherals/user_Login_2.html', {'form':login_form2})


from rest_framework.views import APIView
from rest_framework.response import Response
import json
from django.views.generic.base import TemplateView
from django.views.generic import View
from django.http import JsonResponse

class APIRoot(APIView):
    """
    API Root ...
    """
    def get(self, request):
        data = {
    "customer": "http://localhost:8000/pcp/customer/",
    "product": "http://localhost:8000/pcp/product/",
    "order": "http://localhost:8000/pcp/order/"
        }

        if not request.user.is_superuser:
            data.pop("users")
            data.pop("groups")

        return Response(data)