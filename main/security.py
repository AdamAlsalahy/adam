"""
دوال أمنية مساعدة
"""
import hashlib
import secrets
from django.utils.html import escape
from django.utils.text import slugify
import re


def sanitize_input(user_input, max_length=None):
    """
    تنظيف المدخلات من المستخدم
    """
    if not user_input:
        return ''
    
    # تحويل إلى string
    user_input = str(user_input).strip()
    
    # إزالة أي HTML tags
    user_input = escape(user_input)
    
    # تحديد الطول الأقصى
    if max_length and len(user_input) > max_length:
        user_input = user_input[:max_length]
    
    return user_input


def validate_email(email):
    """
    التحقق من صحة البريد الإلكتروني
    """
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def validate_phone(phone):
    """
    التحقق من صحة رقم الهاتف
    """
    # إزالة المسافات والشرطات
    phone = re.sub(r'[\s\-\(\)]', '', phone)
    
    # التحقق من أن الرقم يحتوي على أرقام فقط
    pattern = r'^[\d\+]{7,20}$'
    return bool(re.match(pattern, phone))


def validate_url(url):
    """
    التحقق من صحة URL
    """
    pattern = r'^https?://[^\s/$.?#].[^\s]*$'
    return bool(re.match(pattern, url, re.IGNORECASE))


def generate_secure_token(length=32):
    """
    إنشاء token عشوائي آمن
    """
    return secrets.token_urlsafe(length)


def hash_password(password):
    """
    تشفير كلمة المرور (يجب استخدام Django's make_password بدلاً منها)
    """
    return hashlib.sha256(password.encode()).hexdigest()


def is_safe_filename(filename):
    """
    التحقق من أن اسم الملف آمن
    """
    # السماح فقط بالأحرف والأرقام والشرطات والنقاط
    pattern = r'^[\w\-. ]+$'
    
    if not re.match(pattern, filename):
        return False
    
    # منع الأسماء الخطرة
    dangerous_names = [
        'con', 'prn', 'aux', 'nul',
        'com1', 'com2', 'com3', 'com4',
        'lpt1', 'lpt2', 'lpt3'
    ]
    
    if filename.lower().split('.')[0] in dangerous_names:
        return False
    
    return True


def get_client_ip(request):
    """
    الحصول على عنوان IP للعميل
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def rate_limit_check(request, key, limit=10, window=3600):
    """
    التحقق من حد معدل الطلبات (Requires Redis)
    """
    # هذا مثال بسيط - في الإنتاج استخدم Redis
    # from django.core.cache import cache
    # cache_key = f"rate_limit:{key}:{get_client_ip(request)}"
    # count = cache.get(cache_key, 0)
    # if count >= limit:
    #     return False
    # cache.set(cache_key, count + 1, window)
    # return True
    pass


def log_security_event(event_type, user, details, severity='INFO'):
    """
    تسجيل حدث أمني
    """
    from .logging_config import security_logger
    
    message = f"[{event_type}] User: {user} | Details: {details}"
    
    if severity == 'CRITICAL':
        security_logger.critical(message)
    elif severity == 'WARNING':
        security_logger.warning(message)
    else:
        security_logger.info(message)
