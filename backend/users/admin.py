from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User

# Зарегистрируем таким нетривиальным способом поле phone в модель админки
fields = list(UserAdmin.fieldsets[1][1]['fields'])
fields.extend(('phone', 'telegram_id'))
UserAdmin.fieldsets[1][1]['fields'] = fields

admin.site.register(User, UserAdmin)
