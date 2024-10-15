#from django import views
from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from Koma import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('', views.home, name='home'),
    path('tickets/create/', views.create_ticket, name='create_ticket'),
    path('user-list/', views.user_list, name='user_list')
]