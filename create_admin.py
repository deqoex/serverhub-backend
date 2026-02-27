import os
import django

# Django ortamını ayarla
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'serverhub.settings')
django.setup()

from apps.users.models import User

# Admin bilgileri
ADMIN_EMAIL = "admin@serverhub.com"
ADMIN_PASS = "Admin123!" 
ADMIN_USER = "admin"

def create_admin():
    try:
        if not User.objects.filter(email=ADMIN_EMAIL).exists():
            User.objects.create_superuser(ADMIN_USER, ADMIN_EMAIL, ADMIN_PASS)
            print(f"✅ Basarili: Admin hesabı olusturuldu ({ADMIN_EMAIL})")
        else:
            print("ℹ️ Bilgi: Admin hesabı zaten mevcut.")
    except Exception as e:
        print(f"❌ Hata: {e}")

if __name__ == "__main__":
    create_admin()
