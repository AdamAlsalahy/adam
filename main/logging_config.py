"""
إعدادات تسجيل الأنشطة (Logging)
"""
import logging
from logging.handlers import RotatingFileHandler
import os

# إنشاء مجلد السجلات إذا لم يكن موجوداً
LOGS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs')
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)


def setup_logging():
    """إعداد نظام التسجيل"""
    
    # إنشاء logger للأمان
    security_logger = logging.getLogger('security')
    security_logger.setLevel(logging.WARNING)
    
    # إنشاء handler للملفات
    security_handler = RotatingFileHandler(
        os.path.join(LOGS_DIR, 'security.log'),
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    
    # إنشاء formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    security_handler.setFormatter(formatter)
    
    # إضافة handler إلى logger
    security_logger.addHandler(security_handler)
    
    # إنشاء logger للأخطاء
    error_logger = logging.getLogger('errors')
    error_logger.setLevel(logging.ERROR)
    
    error_handler = RotatingFileHandler(
        os.path.join(LOGS_DIR, 'errors.log'),
        maxBytes=10485760,  # 10MB
        backupCount=10
    )
    error_handler.setFormatter(formatter)
    error_logger.addHandler(error_handler)
    
    # إنشاء logger للوصول
    access_logger = logging.getLogger('access')
    access_logger.setLevel(logging.INFO)
    
    access_handler = RotatingFileHandler(
        os.path.join(LOGS_DIR, 'access.log'),
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    access_handler.setFormatter(formatter)
    access_logger.addHandler(access_handler)
    
    return security_logger, error_logger, access_logger


# إعداد التسجيل عند استيراد الملف
security_logger, error_logger, access_logger = setup_logging()
