"""
Middleware مخصص لتحسينات الأمان الإضافية
"""
from django.utils.deprecation import MiddlewareMixin
from django.http import HttpResponseForbidden
import logging

logger = logging.getLogger(__name__)


class SecurityHeadersMiddleware(MiddlewareMixin):
    """
    إضافة رؤوس أمان إضافية
    """
    def process_response(self, request, response):
        # منع عرض الموقع في إطار (Clickjacking Protection)
        response['X-Frame-Options'] = 'DENY'
        
        # منع MIME Type Sniffing
        response['X-Content-Type-Options'] = 'nosniff'
        
        # تفعيل XSS Protection
        response['X-XSS-Protection'] = '1; mode=block'
        
        # Referrer Policy
        response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        # Permissions Policy
        response['Permissions-Policy'] = 'geolocation=(), microphone=(), camera=()'
        
        # Strict Transport Security (HSTS) - يجب تفعيله فقط مع HTTPS
        # response['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        
        return response


class RateLimitMiddleware(MiddlewareMixin):
    """
    حماية من الهجمات المتكررة (Brute Force)
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.request_counts = {}
        super().__init__(get_response)
    
    def process_request(self, request):
        # يمكن إضافة منطق تحديد معدل الطلبات هنا
        # هذا مثال بسيط - في الإنتاج استخدم Redis أو قاعدة بيانات
        pass


class InputValidationMiddleware(MiddlewareMixin):
    """
    التحقق من صحة المدخلات
    """
    def process_request(self, request):
        # التحقق من طول URL
        if len(request.path) > 2000:
            logger.warning(f"Suspicious long URL from {request.META.get('REMOTE_ADDR')}")
            return HttpResponseForbidden("Invalid request")
        
        return None


class LoggingMiddleware(MiddlewareMixin):
    """
    تسجيل الأنشطة المريبة
    """
    def process_request(self, request):
        # تسجيل محاولات الوصول إلى المسارات المحظورة
        if request.path.startswith('/admin/') and not request.user.is_staff:
            logger.warning(
                f"Unauthorized admin access attempt from {request.META.get('REMOTE_ADDR')} "
                f"- User: {request.user}"
            )
        
        return None
