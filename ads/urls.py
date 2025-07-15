from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register(r'ads', views.AdViewSet)
router.register(r'proposals', views.ExchangeProposalViewSet, basename='proposal')

app_name = 'ads'

urlpatterns = [
    path('', views.ad_list, name='ad_list'),  # Главная страница со списком объявлений
    path('register/', views.register_view, name='register'),

    # Авторизация/выход
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),

    # Создание объявления
    path('create/', views.create_ad, name='create_ad'),


    # Детали объявления и операции с ним
    path('<int:ad_id>/', views.ad_detail, name='ad_detail'),
    path('<int:ad_id>/edit/', views.edit_ad, name='edit_ad'),
    path('<int:ad_id>/delete/', views.delete_ad, name='delete_ad'),

    # Предложения обмена
    path('exchange/<int:ad_id>/', views.propose_exchange, name='propose_exchange'),
    path('<int:ad_id>/create_exchange_proposal/', views.create_exchange_proposal, name='create_exchange_proposal'),

    # DRF API роутер по адресу /api/
    path('api/', include(router.urls)),
]