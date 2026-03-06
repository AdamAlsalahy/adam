from django.urls import path
from . import views

# اسم التطبيق (يساعدنا لاحقاً في التنقل بين الصفحات)
app_name = 'main'

urlpatterns = [
    # الصفحات الرئيسية
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('services/', views.services, name='services'),
    path('portfolio/', views.portfolio, name='portfolio'),
    path('testimonials/', views.testimonials_view, name='testimonials'),
    path('contact/', views.contact, name='contact'),
    path('faq/', views.faq, name='faq'),
]
