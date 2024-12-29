from django.urls import path
from rest_framework.routers import DefaultRouter
from usuarios.api.views import UsuarioViewSet, login

router = DefaultRouter()
router.register('usuarios', UsuarioViewSet, basename='usuarios')

urlpatterns = [
    path('login/', login, name='login'),  # Ruta para el login
] + router.urls
