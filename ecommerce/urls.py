"""
URL configuration for ecommerce project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from infoHilattis.views import  infoHilattisCreateView, infoHilattisListView, infoHilattisUpdateView
from usuarios.api.views import LoginView, RegisterView, UsuarioDeleteView, UsuarioDetailView, UsuarioListView, UsuarioUpdateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('auth/register', RegisterView.as_view(), name='register'),
    path('auth/login', LoginView.as_view(), name='login'),
    path('usuarios/', UsuarioListView.as_view(), name='usuario-list'),  # Listar usuarios
    path('usuarios/<str:dni>/', UsuarioDetailView.as_view(), name='usuario-detail'),  # Detalle de un usuario
    path('usuarios/<str:dni>/edit/', UsuarioUpdateView.as_view(), name='usuario-update'),  # Editar usuario
    path('usuarios/<str:dni>/delete/', UsuarioDeleteView.as_view(), name='usuario-delete'),  # Eliminar usuario
    path('empresas/', infoHilattisListView.as_view(), name='empresa-list'),  # Listar empresas
    path('empresas/create/', infoHilattisCreateView.as_view(), name='empresa-create'),  # Crear empresa
    path('empresas/<int:id>/', infoHilattisUpdateView.as_view(), name='empresa-edit'),  # Detalle de una empresa
]
