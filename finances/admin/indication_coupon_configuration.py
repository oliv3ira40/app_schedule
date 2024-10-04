from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from finances.models import IndicationCouponConfiguration
from person.models import Client, Professional
from django.shortcuts import redirect
from django.urls import reverse

@admin.register(IndicationCouponConfiguration)
class IndicationCouponConfigurationAdmin(ModelAdmin):
    list_display = ('id_professional', 'type_discount')
    search_fields = ['id_professional__name']
    list_filter = ['id_professional']
    
    # Adiciona o usuário ao get_form
    def get_form_kwargs(self, request, obj=None, **kwargs):
        form_kwargs = super().get_form_kwargs(request, obj, **kwargs)
        form_kwargs['user'] = request.user
        return form_kwargs
    
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        # Se o usuário não for superusuário, remover os campos 'id_professional' e 'id_user'
        if not request.user.is_superuser:
            if 'id_professional' in form.base_fields:
                del form.base_fields['id_professional']

        return form

    def changelist_view(self, request, extra_context=None):
        # Verifica se o usuário é um profissional e se já tem um registro
        if not request.user.is_superuser:
            professional = Professional.objects.filter(id_user=request.user).first()
            try:
                config = IndicationCouponConfiguration.objects.get(id_professional=professional)
                # Se existir, redireciona para a página de edição do registro
                return redirect(reverse('admin:finances_indicationcouponconfiguration_change', args=[config.pk]))
            except IndicationCouponConfiguration.DoesNotExist:
                # Se não existir, redireciona para a criação de um novo registro
                return redirect(reverse('admin:finances_indicationcouponconfiguration_add'))

        # Caso o usuário seja um superusuário, exibe a lista normalmente
        return super().changelist_view(request, extra_context)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            professional = Professional.objects.filter(id_user=request.user).first()
            obj.id_professional = professional
        super().save_model(request, obj, form, change)
