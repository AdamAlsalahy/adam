from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
import os

urlpatterns = [
    # رابط لوحة التحكم
    path('najmat-admin/', admin.site.urls),
    
    # تضمين روابط تطبيق main (موقعنا)
    path('', include('main.urls')),
]

# هذا الكود ضروري جداً لكي تظهر الصور التي ترفعها من لوحة التحكم على جهازك
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# إضافة مسارات robots.txt و sitemap.xml
urlpatterns += [
    path('robots.txt', serve, {'path': 'robots.txt', 'document_root': settings.BASE_DIR}),
    path('sitemap.xml', serve, {'path': 'sitemap.xml', 'document_root': settings.BASE_DIR}),
]