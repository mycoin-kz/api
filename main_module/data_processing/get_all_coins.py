import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")
django.setup()


if __name__ == '__main__':
    from main_module.models import Token
    print(Token)