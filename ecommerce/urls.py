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
from clientes.views import ClienteDeleteView, ClienteDetailByDocumentoView, ClienteListView, ClienteLoginView, RegistroClienteView 
from complaints_book.views import ReclamoCreateView, ReclamoListView
from contact.views import ContactoCreateView, ContactoListView
from cupones.views import CuponCreateView, CuponDeactivateView, CuponDetailView, CuponListView, CuponUpdateView, ValidarCuponView
from empresa.views import EmpresaCreateView, EmpresaDetailView, EmpresaListView, EmpresaUpdateView
from lote.views import LoteCantidadUpdateView, LoteCreateView, LoteDeleteView, LoteListView, LoteUpdateView
from offer.views import PromocionCreateView, PromocionDeleteView, PromocionDetailView, PromocionListView, PromocionUpdateView
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
    path('contact/', ContactoListView.as_view(), name='contacto-list'),
    path('contact/create/', ContactoCreateView.as_view(), name='contacto-create'),
    path('complaints_book/', ReclamoListView.as_view(), name='complaints_book-list'),
    path('complaints_book/create/', ReclamoCreateView.as_view(), name='complaints_book-create'),
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
    path('offer/', PromocionListView.as_view(), name='Promocion-list'),
    path('offer/<int:pk>/', PromocionDetailView.as_view(), name='Promocion-detail'),
    path('offer/create/', PromocionCreateView.as_view(), name='Promocion-create'),
    path('offer/update/<int:pk>/', PromocionUpdateView.as_view(), name='Promocion-update'),
    path('offer/delete/<int:pk>/', PromocionDeleteView.as_view(), name='Promocion-delete'),
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
    path("clientes/registro/", RegistroClienteView.as_view(), name="registro"),
    path("clientes/", ClienteListView.as_view(), name="cliente-list"),
    path("clientes/<str:numero_documento>/", ClienteDetailByDocumentoView.as_view(), name="cliente-detail"),
    path("clientes/<str:numero_documento>/delete/", ClienteDeleteView.as_view(), name="cliente-delete"),
    path("auth/clientes/login/", ClienteLoginView.as_view(), name="cliente-login"),


    path("cupones/", CuponListView.as_view(), name="cupon-list"),
    path("cupones/create/", CuponCreateView.as_view(), name="cupon-create"),
    path("cupones/<int:pk>/", CuponDetailView.as_view(), name="cupon-detail"),
    path("cupones/<int:pk>/update/", CuponUpdateView.as_view(), name="cupon-update"),
    path("cupones/<int:pk>/deactivate/", CuponDeactivateView.as_view(), name="cupon-deactivate"),
    path("cupones/validar/", ValidarCuponView.as_view(), name="cupon-validar"),
    ]