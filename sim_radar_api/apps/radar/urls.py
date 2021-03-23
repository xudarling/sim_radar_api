
from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter
router = SimpleRouter()
router.register('', views.Radar, 'value')

urlpatterns = [
    path('', include(router.urls)),

]
