from rest_framework.routers import DefaultRouter
from usuarios.api.views import UsuarioViewSet

router = DefaultRouter()
router.register('usuarios', UsuarioViewSet, basename='usuarios')
urlpatterns = router.urls