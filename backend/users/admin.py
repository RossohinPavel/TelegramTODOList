from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from users.models import User

# Зарегистрируем таким нетривиальным способом поле phone в модель админки
fields = list(UserAdmin.fieldsets[1][1]['fields'])
fields.append('phone')
UserAdmin.fieldsets[1][1]['fields'] = fields

admin.site.register(User, UserAdmin)
