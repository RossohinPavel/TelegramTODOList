from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User


# Добавление поля с телефоном
try:
    dct = UserAdmin.fieldsets[1][1]
    dct['fields'] = dct['fields'] + ('phone', )
except:
    pass


admin.site.register(User, UserAdmin)
