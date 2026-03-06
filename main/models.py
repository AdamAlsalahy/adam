from django.db import models

# جدول الخدمات (سواتر، واجهات، إلخ)
class Service(models.Model):
    title = models.CharField(max_length=100, verbose_name="اسم الخدمة")
    description = models.TextField(blank=True, verbose_name="وصف الخدمة")
    icon = models.CharField(max_length=50, default="fas fa-check", verbose_name="أيقونة الخدمة")
    order = models.IntegerField(default=0, verbose_name="ترتيب الخدمة")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['order']
        verbose_name = "خدمة"
        verbose_name_plural = "الخدمات"
    
    def __str__(self):
        return self.title


class Portfolio(models.Model):
    # رفع الصورة (غير إجباري)
    image = models.ImageField(upload_to='portfolio/images/', blank=True, null=True, verbose_name="صورة العمل")
    
    # رفع الفيديو (غير إجباري)
    video = models.FileField(upload_to='portfolio/videos/', blank=True, null=True, verbose_name="ملف الفيديو")
    
    # معلومات إضافية
    title = models.CharField(max_length=200, blank=True, verbose_name="عنوان العمل")
    description = models.TextField(blank=True, verbose_name="وصف العمل")
    category = models.CharField(max_length=100, blank=True, verbose_name="فئة العمل")
    order = models.IntegerField(default=0, verbose_name="ترتيب العمل")
    
    date_added = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-order', '-date_added']
        verbose_name = "نموذج عمل"
        verbose_name_plural = "نماذج الأعمال"

    def __str__(self):
        return self.title or f"نموذج عمل رقم {self.id}"


class Testimonial(models.Model):
    """نموذج للتقييمات والآراء من العملاء"""
    client_name = models.CharField(max_length=100, verbose_name="اسم العميل")
    client_company = models.CharField(max_length=100, blank=True, verbose_name="اسم الشركة")
    message = models.TextField(verbose_name="الرسالة")
    rating = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], default=5, verbose_name="التقييم")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, verbose_name="مفعل")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "تقييم"
        verbose_name_plural = "التقييمات"
    
    def __str__(self):
        return f"تقييم من {self.client_name}"


class ContactMessage(models.Model):
    """نموذج لرسائل التواصل من الزوار"""
    name = models.CharField(max_length=100, verbose_name="الاسم")
    email = models.EmailField(verbose_name="البريد الإلكتروني")
    phone = models.CharField(max_length=20, verbose_name="رقم الهاتف")
    subject = models.CharField(max_length=200, verbose_name="الموضوع")
    message = models.TextField(verbose_name="الرسالة")
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False, verbose_name="تم قراءتها")
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = "رسالة تواصل"
        verbose_name_plural = "رسائل التواصل"
    
    def __str__(self):
        return f"رسالة من {self.name}"


class SiteSettings(models.Model):
    """نموذج لإعدادات الموقع"""
    site_title = models.CharField(max_length=200, default="مؤسسة نجمة الإبداع", verbose_name="عنوان الموقع")
    site_description = models.TextField(default="لتركيب وتوريد جميع أنواع زجاج السكريت", verbose_name="وصف الموقع")
    phone = models.CharField(max_length=20, default="0534578698", verbose_name="رقم الهاتف")
    whatsapp = models.CharField(max_length=20, default="966534578698", verbose_name="رقم الواتساب")
    email = models.EmailField(blank=True, verbose_name="البريد الإلكتروني")
    address = models.CharField(max_length=300, default="خميس مشيط - حي الحسام", verbose_name="العنوان")
    facebook = models.URLField(blank=True, verbose_name="رابط فيسبوك")
    instagram = models.URLField(blank=True, verbose_name="رابط إنستجرام")
    twitter = models.URLField(blank=True, verbose_name="رابط تويتر")
    linkedin = models.URLField(blank=True, verbose_name="رابط لينكد إن")
    logo = models.ImageField(upload_to='settings/', blank=True, null=True, verbose_name="شعار الموقع")
    map_iframe_url = models.TextField(blank=True, verbose_name="رابط تضمين الخريطة (Iframe URL)", help_text="انسخ رابط src من كود التضمين في خرائط جوجل")
    
    class Meta:
        verbose_name = "إعدادات الموقع"
        verbose_name_plural = "إعدادات الموقع"
    
    def __str__(self):
        return "إعدادات الموقع"
