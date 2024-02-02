from django.urls import path
from .views import RegisterView, LoginView, UpdateProfileView, LogoutView


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('update-profile/', UpdateProfileView.as_view(), name='update-profile'),
]



























