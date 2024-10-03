from django.contrib import admin
from schedule.models import Package, Service, Session
from person.models import Professional, Client
from unfold.admin import ModelAdmin, TabularInline
from django.utils.translation import gettext_lazy as _

class SessionInline(TabularInline):
    model = Session
    # tab = True
    extra = 0
    fields = ('date', 'status', 'description')
    # ordering = ('date',)
    # classes = ('collapse',)

class ClientRelatedFilter(admin.SimpleListFilter):
    title = _('Cliente')
    parameter_name = 'id_client'

    def lookups(self, request, model_admin):
        user = request.user
        professional = Professional.objects.filter(id_user=user).first()
        if professional:
            clients = Client.objects.filter(id_professional=professional)
            return [(client.id, client.name) for client in clients]
        return []

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(id_client__id=self.value())
        return queryset

class ServiceRelatedFilter(admin.SimpleListFilter):
    title = _('Serviço')
    parameter_name = 'id_service'

    def lookups(self, request, model_admin):
        user = request.user
        professional = Professional.objects.filter(id_user=user).first()
        if professional:
            services = Service.objects.filter(id_professional=professional)
            return [(service.id, service.name) for service in services]
        return []

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(id_service__id=self.value())
        return queryset

@admin.register(Package)
class CustomPackageAdmin(ModelAdmin):

    def count_sessions(self, obj):
        return obj.session_set.count()
    count_sessions.short_description = 'Sessões'

    list_display = ('id_client', 'id_professional', 'id_service', 'value', 'count_sessions', 'closed')
    search_fields = ('id_client__name', 'id_service__name')
    ordering = ('closed',)
    inlines = [SessionInline]
    
    def get_form_kwargs(self, request, obj=None, **kwargs):
        form_kwargs = super().get_form_kwargs(request, obj, **kwargs)
        form_kwargs['user'] = request.user
        return form_kwargs

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
            
            form.base_fields['id_client'].queryset = Client.objects.filter(id_professional__id_user=request.user)
            form.base_fields['id_service'].queryset = Service.objects.filter(id_professional__id_user=request.user)
        return form

    # Se o usuário não for superusuário, removemos 'id_professional' de list_display
    def get_list_display(self, request):
        if not request.user.is_superuser:
            return ('id_client', 'id_service', 'value', 'count_sessions', 'closed')
        return super().get_list_display(request)
    
    # Adiciona filtro de listagem por 'id_professional' caso o usuário seja superusuário
    def get_list_filter(self, request):
        if request.user.is_superuser:
            return ('closed', 'id_professional')
        else: return ('closed', ServiceRelatedFilter, ClientRelatedFilter)

    # Aplica filtros na listagem de acordo com o usuário
    def get_queryset(self, request):
        self.user = request.user
        professional = Professional.objects.filter(id_user=self.user).first()
        clients = Client.objects.filter(id_professional=professional)

        if not self.user.is_superuser:
            return Package.objects.filter(id_professional=professional, id_client__in=clients)
        return super().get_queryset(request)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            professional = Professional.objects.filter(id_user=request.user).first()
            obj.id_professional = professional
        super().save_model(request, obj, form, change)
