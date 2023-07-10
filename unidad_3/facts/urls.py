from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_fact, name='create_fact'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
]
