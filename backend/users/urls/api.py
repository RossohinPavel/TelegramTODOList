from django.urls import path
from .. import views


urlpatterns = [
    path('check_user', views.check_user, name='check_user_api'),
    path('set_telegram_id', views.set_telegram_id, name='set_telegram_id_api')
]