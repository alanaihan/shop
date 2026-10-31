from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
from django.urls import reverse
from django.http import JsonResponse
import requests
from .models import Category, Product, Order, OrderItem, ChatMessage
from .cart import Cart
from .forms import OrderCreateForm, SignUpForm
from django_iranian_payment.contrib.django.services import start_payment, reverify_pending
from django_iranian_payment.core.exceptions import GatewayError


def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)
    return render(request, 'store/product/list.html', {
        'category': category, 'categories': categories, 'products': products,
    })


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    return render(request, 'store/product/detail.html', {'product': product})


@login_required
@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.add(product=product)
    return redirect('store:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'store/cart/detail.html', {'cart': cart})


@require_POST
def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('store:cart_detail')


@require_POST
def cart_update(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    quantity = int(request.POST.get('quantity', 1))
    if quantity > 0:
        cart.add(product=product, quantity=quantity, update_quantity=True)
    else:
        cart.remove(product)
    return redirect('store:cart_detail')


@login_required
def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order, product=item['product'],
                    price=item['price'], quantity=item['quantity']
                )
            cart.clear()
            return render(request, 'store/order/created.html', {'order': order})
    else:
        form = OrderCreateForm()
    return render(request, 'store/order/create.html', {'cart': cart, 'form': form})


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('store:product_list')
    else:
        form = SignUpForm()
    return render(request, 'store/registration/signup.html', {'form': form})


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created')
    return render(request, 'store/order/my_orders.html', {'orders': orders})


@login_required
def payment_start(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if order.paid:
        messages.info(request, 'این سفارش قبلاً پرداخت شده است.')
        return redirect('store:my_orders')
    amount_rial = int(order.get_total_cost() * 10)
    try:
        payment, redirect_url = start_payment(
            "zibal", amount=amount_rial,
            callback_url=request.build_absolute_uri(reverse('store:payment_result', args=[order.id])),
            order_id=str(order.id), description=f'پرداخت سفارش #{order.id}',
        )
        order.amount_sent = amount_rial
        order.save()
        return redirect(redirect_url)
    except GatewayError as e:
        messages.error(request, f'خطا در اتصال به درگاه: {str(e)}')
        return redirect('store:my_orders')


@login_required
def payment_result(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    track_id = request.GET.get('trackId')
    success = request.GET.get('success')
    if success == '1' and track_id:
        try:
            verify_url = "https://gateway.zibal.ir/v1/verify"
            payload = {"merchant": "zibal", "trackId": int(track_id)}
            response = requests.post(verify_url, json=payload, timeout=10)
            result = response.json()
            if result.get('result') in [100, 201]:
                order.paid = True
                order.save()
                messages.success(request, f"پرداخت با موفقیت تایید شد. کد پیگیری: {result.get('refNumber', track_id)}")
            else:
                messages.error(request, f"پرداخت تایید نشد. کد خطا: {result.get('result')}")
        except Exception as e:
            messages.error(request, f"خطا در استعلام از زیبال: {str(e)}")
    else:
        messages.error(request, "پرداخت لغو شد یا ناموفق بود.")
    return render(request, 'store/order/detail.html', {'order': order})


@login_required
def order_delete(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    if request.method == 'POST':
        order.delete()
        messages.success(request, 'سفارش با موفقیت حذف شد.')
    return redirect('store:my_orders')


@login_required
def force_verify_pending(request):
    try:
        reverify_pending()
        messages.success(request, "بررسی مجدد انجام شد.")
    except Exception as e:
        messages.error(request, f"خطا: {str(e)}")
    return redirect('store:my_orders')


def send_chat_message(request):
    if request.method == 'POST':
        message_text = request.POST.get('message', '').strip()
        if message_text:
            ChatMessage.objects.create(
                user=request.user if request.user.is_authenticated else None,
                name=request.user.username if request.user.is_authenticated else 'کاربر مهمان',
                message=message_text
            )
            return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


@login_required
def my_chats(request):
    chats = ChatMessage.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'store/chat/my_chats.html', {'chats': chats})


# 👈 ویو جدید برای گرفتن تاریخچه چت
def get_chat_history(request):
    if request.user.is_authenticated:
        chats = ChatMessage.objects.filter(user=request.user).order_by('created_at')
        data = []
        for chat in chats:
            data.append({
                'message': chat.message,
                'reply': chat.reply,
            })
        return JsonResponse({'status': 'success', 'chats': data})
    return JsonResponse({'status': 'error'}, status=400)