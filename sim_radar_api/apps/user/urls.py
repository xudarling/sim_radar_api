

from django.urls import path, include
from . import views
from rest_framework.routers import SimpleRouter
router = SimpleRouter()
router.register('', views.LoginView, 'login')
router.register('', views.SendSmsView, 'sendsms')
router.register('register', views.RegisterView, 'register')

urlpatterns = [
    path('', include(router.urls)),

]
