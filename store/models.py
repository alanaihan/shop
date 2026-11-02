from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, unique=True)
    class Meta:
        ordering = ('name',)
        verbose_name = 'دسته‌بندی'
        verbose_name_plural = 'دسته‌بندی‌ها'
    def __str__(self): return self.name


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE)
    name = models.CharField(max_length=200, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d', blank=True)
    description = models.TextField(blank=True)
    
    # 👈 این فیلد رو اینجا داری: برچسب اطلاعات (مثلاً آیدی بازی)
    extra_info_label = models.CharField(max_length=100, blank=True, null=True, verbose_name='برچسب اطلاعات اضافی')
    
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ('name',)
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        indexes = [models.Index(fields=['id', 'slug'])]
    def __str__(self): return self.name


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='کاربر')
    first_name = models.CharField(max_length=50, verbose_name='نام')
    last_name = models.CharField(max_length=50, verbose_name='نام خانوادگی')
    phone = models.CharField(max_length=15, verbose_name='شماره تماس')
    address = models.TextField(verbose_name='آدرس')
    
    # 👈 این فیلد رو اینجا داری: جواب کاربر به سوال
    extra_info = models.CharField(max_length=255, blank=True, null=True, verbose_name='اطلاعات اضافی سفارش')
    
    created = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ثبت')
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False, verbose_name='پرداخت شده')
    authority = models.CharField(max_length=255, blank=True, null=True, verbose_name='شناسه پرداخت')
    amount_sent = models.DecimalField(max_digits=12, decimal_places=0, blank=True, null=True, verbose_name='مبلغ ارسالی (ریال)')
    class Meta:
        ordering = ('-created',)
        verbose_name = 'سفارش'
        verbose_name_plural = 'سفارش‌ها'
    def __str__(self): return f'سفارش {self.id}'
    def get_total_cost(self): return sum(item.get_cost() for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE, verbose_name='سفارش')
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE, verbose_name='محصول')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='قیمت')
    quantity = models.PositiveIntegerField(default=1, verbose_name='تعداد')
    class Meta:
        verbose_name = 'آیتم سفارش'
        verbose_name_plural = 'آیتم‌های سفارش'
    def __str__(self): return f'{self.id}'
    def get_cost(self): return self.price * self.quantity


class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='کاربر')
    name = models.CharField(max_length=100, verbose_name='نام کاربر', blank=True, null=True)
    message = models.TextField(verbose_name='پیام کاربر')
    reply = models.TextField(verbose_name='پاسخ ادمین', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ارسال')
    is_read = models.BooleanField(default=False, verbose_name='خوانده شده')
    is_replied = models.BooleanField(default=False, verbose_name='پاسخ داده شده')
    class Meta:
        ordering = ('-created_at',)
        verbose_name = 'پیام پشتیبانی'
        verbose_name_plural = 'پیام‌های پشتیبانی'
    def __str__(self): return f'پیام از {self.name or self.user}'