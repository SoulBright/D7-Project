from django.urls import path
from .views import *

urlpatterns = [
    path('', NewsList.as_view()),  # Список новостей
    path('<int:pk>/', NewsDetails.as_view(), name='news_detail'),  # Контент статьи
    path('categories/', CategoriesList.as_view()),  # Список категорий
    path('categories/subscribe/', PostListByCategories.add_subscribe, name='subscribe'),  # подписка на категорию
    path('categories/unsubscribe/', PostListByCategories.dell_subscribe, name='unsubscribe'),  # отписка от категории
    path('search', post_filter),  # Поиск / Фильтр
    path('add/', PostCreate.as_view(), name='news_create'),  # Создание статьи
    path('<int:pk>/edit/', PostUpdate.as_view(), name='news_update'),  # Редактор статьи
    path('<int:pk>/delete/', PostDelete.as_view(), name='news_delete'),  # Удаление статьи
    path('categories/<int:pk>/', PostListByCategories.as_view(), name='categories_detail'),   # Список статей в категории
    path('user/<int:pk>/', UserDetails.as_view(), name='user_detail'),  # Профиль пользователя
    path('user/<int:pk>/edit/', UserUpdate.as_view(), name='user_update'),  # Редактор профиля
]
