from django.contrib import admin
from .models import Category, Product, Order, OrderItem, ChatMessage

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'price', 'stock', 'available', 'created']
    list_filter = ['available', 'created', 'category']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'user', 'paid', 'created']
    list_filter = ['paid', 'created']
    search_fields = ['first_name', 'last_name', 'phone']

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['order', 'product', 'price', 'quantity']

@admin.register(ChatMessage)
class ChatMessageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'user', 'message', 'reply', 'created_at', 'is_read', 'is_replied']
    list_filter = ['is_read', 'is_replied', 'created_at']
    search_fields = ['message', 'name', 'user__username', 'reply']
    list_editable = ['is_read', 'is_replied']
    readonly_fields = ['created_at', 'message', 'name', 'user']
    fields = ['name', 'user', 'message', 'created_at', 'reply', 'is_read', 'is_replied']