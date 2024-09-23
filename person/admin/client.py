from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from person.models import Client, Professional

from unfold.admin import ModelAdmin

@admin.register(Client)
class CustomClientAdmin(ModelAdmin):
    list_display = ('name', 'email', 'cpf', 'phone', 'birth_date', 'id_user', 'id_professional')
    search_fields = ('name', 'email', 'cpf', 'phone')
    ordering = ('name',)

    # Remove os campos 'id_professional' e 'id_user' do formulário da criação/edição caso o usuário não seja superusuário
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            if 'id_professional' in form.base_fields:
                del form.base_fields['id_professional']
            if 'id_user' in form.base_fields:
                del form.base_fields['id_user']
        return form

    def get_form_kwargs(self, request, obj=None, **kwargs):
        form_kwargs = super().get_form_kwargs(request, obj, **kwargs)
        form_kwargs['user'] = request.user
        return form_kwargs

    def get_list_display(self, request):
        # Se o usuário não for superusuário, removemos 'id_professional' de list_display
        if not request.user.is_superuser:
            return ('name', 'email', 'cpf', 'phone', 'birth_date')
        return super().get_list_display(request)

    def get_queryset(self, request):
        self.user = request.user
        professional = Professional.objects.filter(id_user=self.user).first()
        
        if not self.user.is_superuser:
            return Client.objects.filter(id_professional=professional)
        return super().get_queryset(request)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            professional = Professional.objects.filter(id_user=request.user).first()
            obj.id_professional = professional
        super().save_model(request, obj, form, change)
