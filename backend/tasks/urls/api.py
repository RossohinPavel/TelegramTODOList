from django.urls import path, include
from rest_framework.routers import SimpleRouter
from .. import views


router = SimpleRouter()
router.register('', views.TasksAPIViewSet, basename='tasks')

urlpatterns = [
    path('<int:telegram_id>/', include(router.urls)),
]
