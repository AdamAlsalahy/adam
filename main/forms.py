"""
نماذج آمنة مع التحقق من البيانات
"""
from django import forms
from django.core.exceptions import ValidationError
from .models import ContactMessage
import re


class ContactForm(forms.ModelForm):
    """نموذج التواصل مع التحقق من البيانات"""
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'الاسم الكامل',
                'maxlength': '100'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'البريد الإلكتروني',
                'maxlength': '100'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'رقم الهاتف',
                'maxlength': '20'
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'الموضوع',
                'maxlength': '200'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'الرسالة',
                'rows': 6,
                'maxlength': '5000'
            }),
        }
    
    def clean_name(self):
        """التحقق من الاسم"""
        name = self.cleaned_data.get('name', '').strip()
        
        if not name:
            raise ValidationError('الاسم مطلوب')
        
        if len(name) < 3:
            raise ValidationError('الاسم يجب أن يكون على الأقل 3 أحرف')
        
        if len(name) > 100:
            raise ValidationError('الاسم طويل جداً')
        
        # التحقق من عدم وجود أحرف غريبة
        if not re.match(r'^[\u0600-\u06FFa-zA-Z\s\-\.]+$', name):
            raise ValidationError('الاسم يحتوي على أحرف غير صحيحة')
        
        return name
    
    def clean_email(self):
        """التحقق من البريد الإلكتروني"""
        email = self.cleaned_data.get('email', '').strip().lower()
        
        if not email:
            raise ValidationError('البريد الإلكتروني مطلوب')
        
        # التحقق من صيغة البريد
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            raise ValidationError('صيغة البريد الإلكتروني غير صحيحة')
        
        return email
    
    def clean_phone(self):
        """التحقق من رقم الهاتف"""
        phone = self.cleaned_data.get('phone', '').strip()
        
        if not phone:
            raise ValidationError('رقم الهاتف مطلوب')
        
        # إزالة المسافات والشرطات
        phone = re.sub(r'[\s\-\(\)]', '', phone)
        
        if not re.match(r'^[\d\+]{7,20}$', phone):
            raise ValidationError('صيغة رقم الهاتف غير صحيحة')
        
        return phone
    
    def clean_subject(self):
        """التحقق من الموضوع"""
        subject = self.cleaned_data.get('subject', '').strip()
        
        if not subject:
            raise ValidationError('الموضوع مطلوب')
        
        if len(subject) < 3:
            raise ValidationError('الموضوع يجب أن يكون على الأقل 3 أحرف')
        
        if len(subject) > 200:
            raise ValidationError('الموضوع طويل جداً')
        
        return subject
    
    def clean_message(self):
        """التحقق من الرسالة"""
        message = self.cleaned_data.get('message', '').strip()
        
        if not message:
            raise ValidationError('الرسالة مطلوبة')
        
        if len(message) < 10:
            raise ValidationError('الرسالة يجب أن تكون على الأقل 10 أحرف')
        
        if len(message) > 5000:
            raise ValidationError('الرسالة طويلة جداً')
        
        return message


class ServiceForm(forms.Form):
    """نموذج البحث عن الخدمات"""
    search = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'ابحث عن خدمة...'
        })
    )


class PortfolioFilterForm(forms.Form):
    """نموذج تصفية الأعمال"""
    category = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'اختر الفئة...'
        })
    )
