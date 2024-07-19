from django.contrib import admin
from django.urls import path, include
from django_email_verification import urls as email_urls
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('account/', include('account.urls'), name='account'),
    path('email/', include(email_urls), name='email-verification'),
    path('cart/', include('cart.urls', namespace='cart')),  
    path('payment/', include('payment.urls', namespace='payment')), 
    path('', include('shop.urls', namespace='shop')),
]


urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)