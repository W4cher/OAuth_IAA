from django.urls import path, include
from . import views
from .views import RegistrationView, CustomTokenRefreshView, CustomTokenObtainPairView, CustomLoginView, AuthenticationPage, EmailLoginView
# from .views import *

urlpatterns = [
    path('auth/', AuthenticationPage.as_view(), name='auth_page'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('token/refresh/', CustomTokenRefreshView.as_view()),
    path('token/', CustomTokenObtainPairView.as_view()),
]




