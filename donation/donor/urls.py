from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('make_request/', views.make_request, name='make_request'),
    path('request_view/', views.request_view, name='request_view'),
    path('donors/', views.donors, name='donors'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_view.LoginView.as_view(template_name='donor/login.html'), name='login'),
    path('logout/', auth_view.LogoutView.as_view(template_name='donor/logout.html'), name='logout'),
    path('profile_edit/<int:pk>/', views.profile_edit, name='profile_edit'),


]
