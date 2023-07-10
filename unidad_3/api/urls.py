from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import FactDetail, FactList

urlpatterns = [
    path('auth/', obtain_auth_token),
    path('facts/', FactList.as_view()),
    path('facts/<int:id>/', FactDetail.as_view()),
]
