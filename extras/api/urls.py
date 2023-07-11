from django.urls import path
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import FactDetail, FactList

urlpatterns = [
    path('auth/', TokenObtainPairView.as_view()),
    path('auth/refresh/', TokenRefreshView.as_view()),
    path('facts/', FactList.as_view()),
    path('facts/<int:id>/', FactDetail.as_view()),
]
