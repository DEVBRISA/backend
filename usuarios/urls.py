from django.urls import path
from usuarios import views

urlpatterns = [
    path('', views.render_users, name='users'),
]