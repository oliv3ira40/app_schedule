from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from person.models import Professional

from unfold.admin import ModelAdmin

@admin.register(Professional)
class CustomProfessionalAdmin(ModelAdmin):
    list_display = ('name', 'email', 'cpf', 'phone', 'id_user')
    search_fields = ('name', 'email', 'cpf', 'phone')
    ordering = ('name',)
