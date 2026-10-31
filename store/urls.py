from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart/update/<int:product_id>/', views.cart_update, name='cart_update'),
    path('checkout/', views.order_create, name='order_create'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('my-orders/delete/<int:order_id>/', views.order_delete, name='order_delete'),
    path('payment/start/<int:order_id>/', views.payment_start, name='payment_start'),
    path('payment/result/<int:order_id>/', views.payment_result, name='payment_result'),
    path('chat/send/', views.send_chat_message, name='send_chat_message'),
    # 👈 خط جدید تاریخچه چت
    path('chat/history/', views.get_chat_history, name='get_chat_history'),
    path('my-chats/', views.my_chats, name='my_chats'),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail, name='product_detail'),
]