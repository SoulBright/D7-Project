from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import BaseRegisterView, upgrade_me

urlpatterns = [
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),  # Вход
    path('logout/', LogoutView.as_view(template_name='logout.html'), name='logout'),  # Выход
    path('signup/', BaseRegisterView.as_view(template_name='signup.html'), name='signup'),  # Регистрация
    path('upgrade/', upgrade_me, name='upgrade'),  # Получение премиум аккаунта
]
