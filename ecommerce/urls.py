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
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView

from categoria.views import CategoriaCreateView, CategoriaDeactivateView, CategoriaDeleteView, CategoriaDetailView, CategoriaListView, CategoriaUpdateView, ToggleCategoriaVisibilityView
from empresa.views import EmpresaCreateView, EmpresaDetailView, EmpresaListView, EmpresaUpdateView
from lote.views import LoteCantidadUpdateView, LoteCreateView, LoteDeleteView, LoteListView, LoteUpdateView
from pack.views import PackCreateView, PackDeactivateView, PackDeleteImgView, PackDeleteView, PackDetailView, PackListView, PackUpdateView
from productos.views import ProductoCreateView, ProductoDeactivateView, ProductoDeleteImgView, ProductoDeleteView, ProductoDetailView, ProductoListView, ProductoTogglePackView, ProductoUpdateView
from usuarios.views import RegisterView, LoginView, UsuarioListView, UsuarioDetailView, UsuarioUpdateView, UsuarioChangeStateView, UsuarioDeleteView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    path('auth/register', RegisterView.as_view(), name='register'),
    path('auth/login', LoginView.as_view(), name='login'),
    path('usuarios/', UsuarioListView.as_view(), name='usuario-list'), 
    path('usuarios/<str:dni>', UsuarioDetailView.as_view(), name='usuario-id'),  
    path('usuarios/edit/<str:dni>', UsuarioUpdateView.as_view(), name='usuario-update'), 
    path('usuarios/change-state/<str:dni>', UsuarioChangeStateView.as_view(), name='usuario-change-state'), 
    path('usuarios/delete/<str:dni>', UsuarioDeleteView.as_view(), name='usuario-delete'), 
    path('empresa/', EmpresaListView.as_view(), name='empresa-list'),
    path('empresa/<int:id>', EmpresaDetailView.as_view(), name='empresa-id'),
    path ('empresa/create/', EmpresaCreateView.as_view(), name='empresa-create'),
    path('empresa/update/<int:id>', EmpresaUpdateView.as_view(), name='empresa-update'),
    path('categoria/', CategoriaListView.as_view(), name='categoria-list'),
    path('categoria/<int:id>/', CategoriaDetailView.as_view(), name='categoria-detail'),
    path('categoria/create/', CategoriaCreateView.as_view(), name='categoria-create'),
    path('categoria/update/<int:id>/', CategoriaUpdateView.as_view(), name='categoria-update'),
    path('categoria/deactivate/<int:id>/', CategoriaDeactivateView.as_view(), name='categoria-deactivate'),
    path('categoria/delete/<int:id>/', CategoriaDeleteView.as_view(), name='categoria-delete'),
    path('categoria/toggle-visibility/<int:id>/', ToggleCategoriaVisibilityView.as_view(), name='categoria-toggle-visibility'),
    path('productos/', ProductoListView.as_view(), name='producto-list'),
    path('productos/create/', ProductoCreateView.as_view(), name='producto-create'),
    path('productos/<str:sku>/', ProductoDetailView.as_view(), name='producto-detail'),
    path('productos/update/<str:sku>/', ProductoUpdateView.as_view(), name='producto-update'),
    path('productos/deactivate/<str:sku>/', ProductoDeactivateView.as_view(), name='producto-deactivate'),
    path('productos/delete/<str:sku>/', ProductoDeleteView.as_view(), name='producto-delete'),
    path('productos/delete/img/<str:sku>/', ProductoDeleteImgView.as_view(), name='producto-delete-img'),
    path('productos/activePack/<str:sku>/', ProductoTogglePackView.as_view(), name='producto-pack'),
    path('lote/', LoteListView.as_view(), name='lote-list'),
    path('lote/create/', LoteCreateView.as_view(), name='lote-create'),
    path('lote/update/<int:id>/', LoteUpdateView.as_view(), name='lote-update'),
    path('lote/delete/<int:id>/', LoteDeleteView.as_view(), name='lote-delete'),
    path('lote/update/cantidad/<int:id>/', LoteCantidadUpdateView.as_view(), name='lote-update-cantidad'),
    path('packs/create/', PackCreateView.as_view(), name='pack-create'),
    path('packs/', PackListView.as_view(), name='pack-list'),
    path('packs/<str:sku>/', PackDetailView.as_view(), name='pack-detail'),
    path('packs/update/<str:sku>/', PackUpdateView.as_view(), name='pack-update'),
    path('packs/deactivate/<str:sku>/', PackDeactivateView.as_view(), name='pack-deactivate'),
    path('packs/delete/<str:sku>/', PackDeleteView.as_view(), name='pack-delete'),
    path('packs/delete-img/<str:sku>/', PackDeleteImgView.as_view(), name='pack-delete-img'),
    
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)