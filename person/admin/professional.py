from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from person.models import Professional
from unfold.admin import ModelAdmin
from django.shortcuts import redirect
from django.urls import reverse

@admin.register(Professional)
class CustomProfessionalAdmin(ModelAdmin):
    list_display = ('name', 'email', 'cpf', 'phone', 'id_user')
    search_fields = ('name', 'email', 'cpf', 'phone')
    ordering = ('name',)

    # Adiciona o usuário ao get_form
    def get_form_kwargs(self, request, obj=None, **kwargs):
        form_kwargs = super().get_form_kwargs(request, obj, **kwargs)
        form_kwargs['user'] = request.user
        return form_kwargs

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        # Se o usuário não for superusuário, remover os campos 'id_user'
        if not request.user.is_superuser:
            if 'id_user' in form.base_fields:
                del form.base_fields['id_user']

        return form

    def changelist_view(self, request, extra_context=None):
        # Verifica se o usuário não é superusuário (é um profissional)
        if not request.user.is_superuser:
            professional = Professional.objects.filter(id_user=request.user).first()
            if professional:
                # Se o registro do profissional existir, redireciona para a página de edição
                return redirect(reverse('admin:person_professional_change', args=[professional.pk]))
            else:
                # Se o registro do profissional não existir, redireciona para criar um novo
                return redirect(reverse('admin:person_professional_add'))

        # Caso o usuário seja superusuário, exibe a lista normalmente
        return super().changelist_view(request, extra_context)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            obj.id_user = request.user
        super().save_model(request, obj, form, change)
