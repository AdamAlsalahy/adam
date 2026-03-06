# دليل النشر (Deployment) - مؤسسة نجمة الإبداع

## المتطلبات

- Server بنظام Linux (Ubuntu 20.04 أو أحدث)
- Python 3.8+
- Nginx أو Apache
- PostgreSQL (اختياري لكن موصى به)
- SSL Certificate

## خطوات النشر

### 1. إعداد الخادم

```bash
# تحديث النظام
sudo apt update
sudo apt upgrade -y

# تثبيت المتطلبات
sudo apt install -y python3 python3-pip python3-venv git nginx postgresql postgresql-contrib
```

### 2. استنساخ المشروع

```bash
# الانتقال إلى مجلد التطبيقات
cd /var/www

# استنساخ المشروع
sudo git clone https://github.com/yourusername/najmat.git
cd najmat

# تغيير الصلاحيات
sudo chown -R $USER:$USER /var/www/najmat
```

### 3. إنشاء بيئة افتراضية

```bash
# إنشاء البيئة الافتراضية
python3 -m venv venv

# تفعيل البيئة
source venv/bin/activate

# تحديث pip
pip install --upgrade pip

# تثبيت المتطلبات
pip install -r requirements.txt
```

### 4. إعداد قاعدة البيانات

```bash
# إنشاء قاعدة بيانات PostgreSQL
sudo -u postgres psql

# داخل psql:
CREATE DATABASE najmat_db;
CREATE USER najmat_user WITH PASSWORD 'strong_password_here';
ALTER ROLE najmat_user SET client_encoding TO 'utf8';
ALTER ROLE najmat_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE najmat_user SET default_transaction_deferrable TO on;
ALTER ROLE najmat_user SET timezone TO 'UTC';
GRANT ALL PRIVILEGES ON DATABASE najmat_db TO najmat_user;
\q
```

### 5. إعداد متغيرات البيئة

```bash
# نسخ ملف البيئة
cp .env.example .env

# تعديل ملف .env
nano .env
```

**محتوى .env للإنتاج:**
```
DEBUG=False
SECRET_KEY=your-very-long-random-secret-key-here
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=najmat_db
DB_USER=najmat_user
DB_PASSWORD=strong_password_here
DB_HOST=localhost
DB_PORT=5432

# Security
SECURE_SSL_REDIRECT=True
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
```

### 6. تطبيق الهجرات

```bash
# تفعيل البيئة الافتراضية
source venv/bin/activate

# تطبيق الهجرات
python manage.py migrate

# جمع الملفات الثابتة
python manage.py collectstatic --noinput

# إنشاء مستخدم المسؤول
python manage.py createsuperuser

# إنشاء البيانات التجريبية (اختياري)
python manage.py populate_data
```

### 7. إعداد Gunicorn

```bash
# تثبيت Gunicorn
pip install gunicorn

# اختبار Gunicorn
gunicorn core.wsgi:application --bind 0.0.0.0:8000

# إنشاء ملف خدمة Gunicorn
sudo nano /etc/systemd/system/gunicorn.service
```

**محتوى gunicorn.service:**
```ini
[Unit]
Description=gunicorn daemon for najmat
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/var/www/najmat
ExecStart=/var/www/najmat/venv/bin/gunicorn \
          --workers 3 \
          --bind unix:/var/www/najmat/gunicorn.sock \
          core.wsgi:application

[Install]
WantedBy=multi-user.target
```

```bash
# تفعيل الخدمة
sudo systemctl daemon-reload
sudo systemctl start gunicorn
sudo systemctl enable gunicorn
```

### 8. إعداد Nginx

```bash
# إنشاء ملف إعدادات Nginx
sudo nano /etc/nginx/sites-available/najmat
```

**محتوى إعدادات Nginx:**
```nginx
upstream gunicorn {
    server unix:/var/www/najmat/gunicorn.sock fail_timeout=0;
}

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;
    
    # إعادة التوجيه إلى HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com www.yourdomain.com;
    
    # SSL Certificate
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # SSL Configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;
    
    client_max_body_size 20M;
    
    location = /favicon.ico {
        access_log off;
        log_not_found off;
    }
    
    location /static/ {
        alias /var/www/najmat/staticfiles/;
        expires 30d;
    }
    
    location /media/ {
        alias /var/www/najmat/media/;
        expires 7d;
    }
    
    location / {
        proxy_pass http://gunicorn;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
# تفعيل الموقع
sudo ln -s /etc/nginx/sites-available/najmat /etc/nginx/sites-enabled/
sudo rm /etc/nginx/sites-enabled/default

# اختبار إعدادات Nginx
sudo nginx -t

# إعادة تشغيل Nginx
sudo systemctl restart nginx
```

### 9. إعداد SSL Certificate (Let's Encrypt)

```bash
# تثبيت Certbot
sudo apt install -y certbot python3-certbot-nginx

# الحصول على شهادة SSL
sudo certbot certonly --standalone -d yourdomain.com -d www.yourdomain.com

# تجديد تلقائي
sudo systemctl enable certbot.timer
sudo systemctl start certbot.timer
```

### 10. إعداد النسخ الاحتياطية

```bash
# إنشاء مجلد النسخ الاحتياطية
mkdir -p /var/backups/najmat

# إنشاء سكريبت النسخ الاحتياطية
sudo nano /usr/local/bin/backup-najmat.sh
```

**محتوى سكريبت النسخ الاحتياطية:**
```bash
#!/bin/bash

BACKUP_DIR="/var/backups/najmat"
DATE=$(date +%Y%m%d_%H%M%S)
DB_NAME="najmat_db"
DB_USER="najmat_user"

# نسخ احتياطية لقاعدة البيانات
pg_dump -U $DB_USER $DB_NAME > $BACKUP_DIR/db_backup_$DATE.sql

# نسخ احتياطية للملفات المرفوعة
tar -czf $BACKUP_DIR/media_backup_$DATE.tar.gz /var/www/najmat/media/

# حذف النسخ الاحتياطية القديمة (أكثر من 30 يوم)
find $BACKUP_DIR -type f -mtime +30 -delete

echo "Backup completed: $DATE"
```

```bash
# جعل السكريبت قابل للتنفيذ
sudo chmod +x /usr/local/bin/backup-najmat.sh

# إضافة إلى cron للتنفيذ اليومي
sudo crontab -e
# أضف: 0 2 * * * /usr/local/bin/backup-najmat.sh
```

### 11. مراقبة الموقع

```bash
# تثبيت Supervisor لمراقبة Gunicorn
sudo apt install -y supervisor

# إنشاء ملف إعدادات Supervisor
sudo nano /etc/supervisor/conf.d/najmat.conf
```

**محتوى إعدادات Supervisor:**
```ini
[program:gunicorn]
directory=/var/www/najmat
command=/var/www/najmat/venv/bin/gunicorn core.wsgi:application --bind unix:/var/www/najmat/gunicorn.sock
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/gunicorn.log
```

```bash
# تحديث Supervisor
sudo supervisorctl reread
sudo supervisorctl update
```

## التحقق من الموقع

```bash
# التحقق من حالة Gunicorn
sudo systemctl status gunicorn

# التحقق من حالة Nginx
sudo systemctl status nginx

# عرض السجلات
tail -f /var/log/gunicorn.log
tail -f /var/log/nginx/error.log
```

## تحديث الموقع

```bash
# سحب التحديثات الجديدة
cd /var/www/najmat
git pull origin main

# تفعيل البيئة الافتراضية
source venv/bin/activate

# تثبيت المتطلبات الجديدة
pip install -r requirements.txt

# تطبيق الهجرات
python manage.py migrate

# جمع الملفات الثابتة
python manage.py collectstatic --noinput

# إعادة تشغيل Gunicorn
sudo systemctl restart gunicorn
```

## استكشاف الأخطاء

### الموقع لا يعمل
```bash
# التحقق من حالة الخدمات
sudo systemctl status gunicorn
sudo systemctl status nginx

# عرض السجلات
tail -f /var/log/gunicorn.log
tail -f /var/log/nginx/error.log
```

### مشاكل قاعدة البيانات
```bash
# التحقق من اتصال PostgreSQL
psql -U najmat_user -d najmat_db -h localhost

# إعادة تشغيل PostgreSQL
sudo systemctl restart postgresql
```

### مشاكل الملفات الثابتة
```bash
# جمع الملفات الثابتة مرة أخرى
python manage.py collectstatic --clear --noinput

# التحقق من الصلاحيات
sudo chown -R www-data:www-data /var/www/najmat
```

## الأداء والتحسينات

### تحسين سرعة الموقع
```bash
# تفعيل Gzip في Nginx
# أضف إلى /etc/nginx/nginx.conf:
gzip on;
gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
gzip_min_length 1000;
```

### استخدام CDN
- استخدم CloudFlare أو Akamai لتسريع الموقع

### تحسين قاعدة البيانات
```bash
# إنشاء فهارس
python manage.py shell
from django.db import connection
connection.cursor().execute("CREATE INDEX idx_portfolio_category ON main_portfolio(category);")
```

## الدعم والمساعدة

للحصول على دعم في النشر:
- البريد الإلكتروني: support@najmat.com
- الهاتف: +966-534-578-698

---

**آخر تحديث**: 2026-03-04
**الإصدار**: 1.0
