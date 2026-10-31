#!/usr/bin/env bash
# Exit on error
set -o errexit

# نصب کتابخانه‌ها
pip install -r requirements.txt

# جمع‌آوری فایل‌های استاتیک
python manage.py collectstatic --no-input

# اجرای migration ها
python manage.py migrate