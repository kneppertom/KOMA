# Koma/admin.py

from django.contrib import admin
from .models import Ticket, TicketHistory, Module, ModuleManager, UserProfile, Login

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'status', 'created_at')
    search_fields = ('title', 'description', 'created_by__username')
    list_filter = ('status', 'priority')

@admin.register(Module)
class ModuleAdmin(admin.ModelAdmin):
    list_display = ('name', 'short_name')

@admin.register(ModuleManager)
class ModuleManagerAdmin(admin.ModelAdmin):
    list_display = ('module', 'user')

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'service_level')

@admin.register(Login)
class LoginAdmin(admin.ModelAdmin):
    list_display = ('username', 'user')

@admin.register(TicketHistory)
class TicketHistoryAdmin(admin.ModelAdmin):
    list_display = ('ticket', 'user', 'datetime')
    list_filter = ('datetime',)
