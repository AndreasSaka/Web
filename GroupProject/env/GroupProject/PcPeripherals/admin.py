from django.contrib import admin
from .models import Customer, ProductCategory, Product, Order, OrderItem, ShippingAddress

'''Register all models to the admin site'''

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')
    ordering = ('-last_name',)
    search_fields = ('first_name', 'last_name', 'email')


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('category',)
    ordering = ('category',)
    search_fields = ('category',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('category', 'name', 'price')
    ordering = ('-name',)
    search_fields = ('category', 'name', 'price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'date_ordered', 'complete', 'transaction_id')
    ordering = ('customer',)
    search_fields = ('customer', 'date_ordered', 'complete', 'transaction_id')


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'order', 'quantity', 'date_added')
    ordering = ('product',)
    search_fields = ('product', 'order', 'quantity', 'date_added')


@admin.register(ShippingAddress)
class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('customer', 'order', 'address', 'city', 'zipcode', 'date_added')
    ordering = ('customer',)
    search_fields = ('customer', 'order', 'address', 'city', 'zipcode', 'date_added')
