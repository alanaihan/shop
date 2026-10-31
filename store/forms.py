from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Order, ChatMessage


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['first_name', 'last_name', 'phone', 'address']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'نام', 'class': 'form-control bg-dark text-light border-secondary', 'style': 'padding: 10px;'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'نام خانوادگی', 'class': 'form-control bg-dark text-light border-secondary', 'style': 'padding: 10px;'}),
            'phone': forms.TextInput(attrs={'placeholder': 'شماره تماس', 'class': 'form-control bg-dark text-light border-secondary', 'style': 'padding: 10px;'}),
            'address': forms.Textarea(attrs={'placeholder': 'آدرس کامل', 'rows': 3, 'class': 'form-control bg-dark text-light border-secondary', 'style': 'padding: 10px;'}),
        }


class SignUpForm(UserCreationForm):
    email = forms.EmailField(max_length=254, help_text='الزامی است. یک ایمیل معتبر وارد کنید.', widget=forms.EmailInput(attrs={'class': 'form-control bg-dark text-light border-secondary', 'style': 'padding: 10px;'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs.update({'class': 'form-control bg-dark text-light border-secondary', 'style': 'padding: 10px;'})


# 👈 فرم جدید برای ارسال پیام چت
class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ['message']
        widgets = {
            'message': forms.TextInput(attrs={'placeholder': 'پیام خود را بنویسید...', 'class': 'form-control', 'id': 'chatInput'}),
        }