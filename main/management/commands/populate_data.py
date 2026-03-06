"""
أمر لإنشاء بيانات تجريبية للموقع
استخدام: python manage.py populate_data
"""
from django.core.management.base import BaseCommand
from main.models import Service, Testimonial, SiteSettings


class Command(BaseCommand):
    help = 'إنشاء بيانات تجريبية للموقع'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('بدء إنشاء البيانات التجريبية...'))

        # إنشاء الخدمات
        services_data = [
            {
                'title': 'تركيب السواتر الزجاجية',
                'description': 'تركيب احترافي للسواتر الزجاجية بجميع أنواعها وأحجامها',
                'order': 1
            },
            {
                'title': 'الواجهات الزجاجية',
                'description': 'تصميم وتركيب واجهات زجاجية حديثة وأنيقة',
                'order': 2
            },
            {
                'title': 'الأبواب والنوافذ',
                'description': 'توريد وتركيب أبواب ونوافذ زجاجية عالية الجودة',
                'order': 3
            },
            {
                'title': 'الأسقف الزجاجية',
                'description': 'تركيب أسقف زجاجية لإضاءة طبيعية أفضل',
                'order': 4
            },
            {
                'title': 'الأقسام الزجاجية',
                'description': 'تصميم وتركيب أقسام زجاجية للمكاتب والمحلات',
                'order': 5
            },
            {
                'title': 'الصيانة والإصلاح',
                'description': 'خدمات صيانة دورية وإصلاح سريع للزجاج',
                'order': 6
            },
        ]

        for service_data in services_data:
            service, created = Service.objects.get_or_create(
                title=service_data['title'],
                defaults={
                    'description': service_data['description'],
                    'order': service_data['order']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ تم إنشاء الخدمة: {service.title}'))
            else:
                self.stdout.write(f'- الخدمة موجودة بالفعل: {service.title}')

        # إنشاء التقييمات
        testimonials_data = [
            {
                'client_name': 'أحمد محمد',
                'client_company': 'شركة الأمل للتجارة',
                'message': 'خدمة ممتازة وجودة عالية جداً. فريق احترافي وملتزم بالمواعيد.',
                'rating': 5
            },
            {
                'client_name': 'فاطمة علي',
                'client_company': 'مركز الجمال والعناية',
                'message': 'تركيب رائع وتصميم جميل. أنصح بشدة بالتعامل معهم.',
                'rating': 5
            },
            {
                'client_name': 'محمود حسن',
                'client_company': 'مكتب الاستشارات الهندسية',
                'message': 'أسعار منافسة وجودة عالية. استجابة سريعة للطلبات.',
                'rating': 4
            },
            {
                'client_name': 'سارة خالد',
                'client_company': 'متجر الملابس الفاخرة',
                'message': 'تجربة رائعة من البداية إلى النهاية. شكراً على الاحترافية.',
                'rating': 5
            },
            {
                'client_name': 'علي إبراهيم',
                'client_company': 'مطعم النخيل',
                'message': 'عمل احترافي وتركيب متقن. الفريق متعاون جداً.',
                'rating': 5
            },
        ]

        for testimonial_data in testimonials_data:
            testimonial, created = Testimonial.objects.get_or_create(
                client_name=testimonial_data['client_name'],
                defaults={
                    'client_company': testimonial_data['client_company'],
                    'message': testimonial_data['message'],
                    'rating': testimonial_data['rating'],
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✓ تم إنشاء تقييم من: {testimonial.client_name}'))
            else:
                self.stdout.write(f'- التقييم موجود بالفعل: {testimonial.client_name}')

        # إنشاء أو تحديث إعدادات الموقع
        site_settings, created = SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                'site_title': 'مؤسسة نجمة الإبداع',
                'site_description': 'متخصصة في تركيب وتوريد جميع أنواع زجاج السكريت',
                'phone': '0534578698',
                'whatsapp': '966534578698',
                'email': 'info@najmat.com',
                'address': 'خميس مشيط - حي الحسام',
                'facebook': 'https://facebook.com/najmat',
                'instagram': 'https://instagram.com/najmat',
                'twitter': 'https://twitter.com/najmat',
            }
        )

        if created:
            self.stdout.write(self.style.SUCCESS('✓ تم إنشاء إعدادات الموقع'))
        else:
            self.stdout.write('- إعدادات الموقع موجودة بالفعل')

        self.stdout.write(self.style.SUCCESS('\n✅ تم إنشاء البيانات التجريبية بنجاح!'))
