from django.urls import path

from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('<int:fact_id>/', views.fact_view, name='fact'),
    path('random/', views.random_view, name='random'),
]
