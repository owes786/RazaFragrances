from django.contrib import admin
from .models import Product, Review ,OrderDetails, Cart, Customer_Details, Wishlist, Buy_now_model
from django.utils.html import format_html
from django.urls import reverse


# Register your models here.
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['id', 'Title','Brand', 'Mrp', 'Selling_Price', 'Description', 'Category', 'Product_Image']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'Product', 'Review_Description', 'image', 'Date']


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'Product']


@admin.register(Customer_Details)
class CustomerDetailsAdmin(admin.ModelAdmin):
    list_display = ['id', 'user' ,'Name', 'Mobile_Number', 'Pincode', 'City', 'Address', 'State', 'Landmark']


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'Product', 'quantity']


@admin.register(Buy_now_model)
class Buy_nowAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'Product', 'quantity']


@admin.register(OrderDetails)
class OrderDetailsAdmin(admin.ModelAdmin):
    list_display = ['id', 'Name', 'Title', 'Quantity' ,'Total_Amount','OrderDate', 'Prepaid', 'Status']
