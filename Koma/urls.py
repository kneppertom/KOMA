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
    path('user-list/', views.user_list, name='user_list'),
    #path('tickets/', views.ticket_form, name='ticket_form'),
    path('ticket-list/', views.ticket_list, name='ticket_list'),
    path('tickets/', views.ticket_overview, name='ticket_overview'),
    path('get_ticket/<int:ticket_id>/', views.get_ticket, name='get_ticket'),
    path('edit_ticket/<int:ticket_id>/', views.edit_ticket, name='edit_ticket'),
    path('get_ticket/<int:ticket_id>/', views.get_ticket, name='get_ticket'),
    path('update_ticket/<int:ticket_id>/', views.update_ticket, name='update_ticket'),
    path('create_ticket/', views.create_ticket, name='create_ticket'),
    path('statistic_overview/', views.statistic_overview, name='statistic_overview'),
    path('add_remark/<int:ticket_id>/', views.add_remark, name='add_remark'),
]