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


from categoria.views import CategoriaCreateView, CategoriaDeleteView, CategoriaEditView, CategoriaIdView, CategoriaListView
from infoHilattis.views import  infoHilattisCreateView, infoHilattisListView, infoHilattisUpdateView
from projects.views import CreateProjectView, DeleteImageView, DeleteProjectView, EditProjectView, ListProjectView, ProjectIdView
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
    path('usuarios/', UsuarioListView.as_view(), name='usuario-list'), 
    path('usuarios/<str:dni>', UsuarioDetailView.as_view(), name='usuario-detail'),  
    path('usuarios/edit/<str:dni>', UsuarioUpdateView.as_view(), name='usuario-update'),  
    path('usuarios/delete/<str:dni>', UsuarioDeleteView.as_view(), name='usuario-delete'), 
    path('empresas/', infoHilattisListView.as_view(), name='empresa-list'), 
    path('empresas/create', infoHilattisCreateView.as_view(), name='empresa-create'),     
    path('empresas/edit/<int:id>', infoHilattisUpdateView.as_view(), name='empresa-edit'),
    path('categorias/create', CategoriaCreateView.as_view(), name='categoria-create'),
    path('categorias/', CategoriaListView.as_view(), name='categoria-list'),
    path('categorias/<int:id>', CategoriaIdView.as_view(), name='categoria-id'),
    path('categorias/edit/<int:id>', CategoriaEditView.as_view(), name='categoria-edit'),
    path('categorias/delete/<int:id>', CategoriaDeleteView.as_view(), name='categoria-delete'),
    path('projects/', ListProjectView.as_view(), name='list_projects'),
    path('projects/create', CreateProjectView.as_view(), name='create_project'),
    path('projects/<int:id>', ProjectIdView.as_view(), name='get_project_by_id'),
    path('projects/edit/<int:id>', EditProjectView.as_view(), name='edit_project'),
    path('projects/delete/<int:id>', DeleteProjectView.as_view(), name='delete_project'),
    path('projects/delete-images/<int:id>', DeleteImageView.as_view(), name='delete_project_images'),
    ]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)