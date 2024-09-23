from django.contrib import admin
from schedule.models import Service
from person.models import Professional
from unfold.admin import ModelAdmin

@admin.register(Service)
class CustomServiceAdmin(ModelAdmin):
    list_display = ('name', 'average_duration', 'average_price', 'id_professional')
    search_fields = ('name',)
    ordering = ('name',)

    # Adiciona o usuário ao get_form
    def get_form_kwargs(self, request, obj=None, **kwargs):
        form_kwargs = super().get_form_kwargs(request, obj, **kwargs)
        form_kwargs['user'] = request.user
        return form_kwargs

    # Remove os campos 'id_professional' e 'id_user' do formulário da criação/edição caso o usuário não seja superusuário
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if not request.user.is_superuser:
            if 'id_professional' in form.base_fields:
                del form.base_fields['id_professional']
        return form

    # Se o usuário não for superusuário, removemos 'id_professional' de list_display
    def get_list_display(self, request):
        if not request.user.is_superuser:
            return ('name', 'average_duration', 'average_price')
        return super().get_list_display(request)
    
    # Adiciona filtro de listagem por 'id_professional' caso o usuário seja superusuário
    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ('id_professional',)
        else: return ()

    def get_queryset(self, request):
        self.user = request.user
        professional = Professional.objects.filter(id_user=self.user).first()

        if not self.user.is_superuser:
            return Service.objects.filter(id_professional=professional)
        return super().get_queryset(request)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            professional = Professional.objects.filter(id_user=request.user).first()
            obj.id_professional = professional
        super().save_model(request, obj, form, change)
