from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from .models import Service, Portfolio, Testimonial, ContactMessage, SiteSettings

def get_site_settings():
    """الحصول على إعدادات الموقع أو إنشاء إعدادات افتراضية"""
    settings, created = SiteSettings.objects.get_or_create(pk=1)
    return settings

def home(request):
    """الصفحة الرئيسية"""
    services = Service.objects.all()
    portfolios = Portfolio.objects.all()[:6]  # عرض أول 6 أعمال فقط
    testimonials = Testimonial.objects.filter(is_active=True)[:3]
    site_settings = get_site_settings()
    
    context = {
        'services': services,
        'portfolios': portfolios,
        'testimonials': testimonials,
        'site_settings': site_settings,
    }
    return render(request, 'main/home.html', context)


def about(request):
    """صفحة من نحن"""
    site_settings = get_site_settings()
    services = Service.objects.all()
    
    context = {
        'site_settings': site_settings,
        'services': services,
    }
    return render(request, 'main/about.html', context)


def services(request):
    """صفحة الخدمات"""
    services = Service.objects.all()
    site_settings = get_site_settings()
    
    context = {
        'services': services,
        'site_settings': site_settings,
    }
    return render(request, 'main/services.html', context)


def portfolio(request):
    """صفحة المعرض"""
    portfolios = Portfolio.objects.all()
    categories = Portfolio.objects.values_list('category', flat=True).distinct()
    category = request.GET.get('category')
    
    if category:
        portfolios = portfolios.filter(category=category)
    
    site_settings = get_site_settings()
    
    context = {
        'portfolios': portfolios,
        'categories': categories,
        'selected_category': category,
        'site_settings': site_settings,
    }
    return render(request, 'main/portfolio.html', context)


def testimonials_view(request):
    """صفحة التقييمات"""
    testimonials = Testimonial.objects.filter(is_active=True)
    site_settings = get_site_settings()
    
    context = {
        'testimonials': testimonials,
        'site_settings': site_settings,
    }
    return render(request, 'main/testimonials.html', context)


@require_http_methods(["GET", "POST"])
def contact(request):
    """صفحة التواصل ومعالجة النموذج"""
    site_settings = get_site_settings()
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        subject = request.POST.get('subject', '').strip()
        message_text = request.POST.get('message', '').strip()
        
        # التحقق من البيانات
        if name and email and phone and subject and message_text:
            try:
                ContactMessage.objects.create(
                    name=name,
                    email=email,
                    phone=phone,
                    subject=subject,
                    message=message_text
                )
                messages.success(request, 'تم استلام رسالتك بنجاح! سنتواصل معك قريباً.')
                return redirect('main:contact')
            except Exception as e:
                messages.error(request, 'حدث خطأ في إرسال الرسالة. يرجى المحاولة لاحقاً.')
        else:
            messages.error(request, 'يرجى ملء جميع الحقول المطلوبة.')
    
    context = {
        'site_settings': site_settings,
    }
    return render(request, 'main/contact.html', context)


def faq(request):
    """صفحة الأسئلة الشائعة"""
    site_settings = get_site_settings()
    
    faqs = [
        {
            'question': 'ما هي أنواع الزجاج المتوفرة لديكم؟',
            'answer': 'لدينا مجموعة واسعة من أنواع الزجاج السكريت بمختلف الألوان والسمك والتصاميم التي تناسب احتياجاتك.'
        },
        {
            'question': 'هل تقدمون خدمات التركيب؟',
            'answer': 'نعم، نقدم خدمات التركيب الاحترافية من قبل فريق متخصص وذو خبرة عالية.'
        },
        {
            'question': 'ما هو سعر التوصيل والتركيب؟',
            'answer': 'يتم حساب السعر بناءً على الموقع والحجم والنوع. يرجى التواصل معنا للحصول على تسعيرة دقيقة.'
        },
        {
            'question': 'هل لديكم ضمان على المنتجات؟',
            'answer': 'نعم، جميع منتجاتنا مضمونة وتتمتع بضمان شامل ضد العيوب الصناعية.'
        },
        {
            'question': 'كم الوقت المستغرق للتركيب؟',
            'answer': 'يعتمد الوقت على حجم المشروع، لكن عادة ما يتم إنجاز المشاريع الصغيرة في يوم واحد.'
        },
        {
            'question': 'هل تقدمون استشارات تصميم مجانية؟',
            'answer': 'نعم، نقدم استشارات تصميم مجانية لمساعدتك في اختيار أفضل حل لاحتياجاتك.'
        },
    ]
    
    context = {
        'faqs': faqs,
        'site_settings': site_settings,
    }
    return render(request, 'main/faq.html', context)
