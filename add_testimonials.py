import os
import sys
import django

# Add project root to sys.path
project_root = os.path.dirname(os.path.abspath(__file__))
if project_root not in sys.path:
    sys.path.append(project_root)

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from main.models import Testimonial

testimonials_data = [
    {
        "client_name": "أحمد الشهراني",
        "client_company": "فيلا خاصة",
        "message": "عمل احترافي جداً في تركيب واجهات الزجاج السكريت لمنزلي. الجودة عالية والالتزام بالمواعيد كان مبهراً.",
        "rating": 5
    },
    {
        "client_name": "محمد القحطاني",
        "client_company": "مجموعة القوافل التجارية",
        "message": "تعاملنا مع مؤسسة نجمة الإبداع في تركيب أبواب زجاجية للمكتب. سرعة في التنفيذ وفريق عمل متعاون جداً.",
        "rating": 5
    },
    {
        "client_name": "خالد العتيبي",
        "client_company": "مطعم مذاق الخليج",
        "message": "أفضل مؤسسة في منطقة عسير لتركيب زجاج السكريت. الدقة في المقاسات واللمسات النهائية ممتازة.",
        "rating": 5
    },
    {
        "client_name": "صالح العمري",
        "client_company": "عمارة سكنية",
        "message": "الأسعار منافسة جداً مقارنة بالجودة المقدمة. أنصح بالتعامل معهم لمن يبحث عن الإتقان.",
        "rating": 5
    },
    {
        "client_name": "عبد الله عسيري",
        "client_company": "مركز فجر التجاري",
        "message": "تم تركيب واجهات كاملة للمركز في وقت قياسي. العمل متقن جداً والضمان حقيقي.",
        "rating": 5
    }
]

for data in testimonials_data:
    obj, created = Testimonial.objects.get_or_create(
        client_name=data['client_name'],
        defaults={
            'client_company': data['client_company'],
            'message': data['message'],
            'rating': data['rating'],
            'is_active': True
        }
    )
    if not created:
        obj.message = data['message']
        obj.client_company = data['client_company']
        obj.rating = data['rating']
        obj.save()

print("Successfully added/updated testimonials.")
