from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from store import views as store_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('accounts/login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/signup/', store_views.signup, name='signup'),
    
    # 👈 آدرس‌های خود کتابخانه (callback زرین‌پال/زیبال)
    path('payment/', include('django_iranian_payment.contrib.django.urls')),
    
    path('', include('store.urls', namespace='store')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)