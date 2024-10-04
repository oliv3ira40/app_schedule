from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
from finances.models import DiscountCoupon
from person.models import Client, Professional

@admin.register(DiscountCoupon)
class DiscountCouponAdmin(ModelAdmin):
    list_display = ('code', 'used', 'type_discount', 'cancelled', 'id_client', 'id_professional')
    search_fields = ('code', 'id_client__name', 'id_professional__name')
    list_filter = ('used', 'cancelled', 'type_discount')
    readonly_fields = ['used']
    ordering = ('-created_at',)

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

            try:
                # Obtem o profissional atual
                professional = Professional.objects.get(id_user=request.user)
                
                # Filtrar os clientes do profissional atual
                queryset = Client.objects.filter(id_professional=professional)
                if obj:  # Se estiver editando, excluir o próprio cliente da lista de indicados
                    queryset = queryset.exclude(id=obj.id)
                
                form.base_fields['id_client'].queryset = queryset
            except Professional.DoesNotExist:
                # Se o profissional não existir, deixar o queryset de 'id_client' vazio
                form.base_fields['id_client'].queryset = Client.objects.none()

        return form

    def get_list_display(self, request):
        # Se o usuário não for superusuário, removemos 'id_professional' de list_display
        if not request.user.is_superuser:
            return ('code', 'used', 'type_discount', 'cancelled', 'id_client')
        return super().get_list_display(request)
    
    def get_queryset(self, request):
        self.user = request.user
        professional = Professional.objects.filter(id_user=self.user).first()
        
        if not self.user.is_superuser:
            return DiscountCoupon.objects.filter(id_professional=professional)
        return super().get_queryset(request)

    def save_model(self, request, obj, form, change):
        if not request.user.is_superuser:
            professional = Professional.objects.filter(id_user=request.user).first()
            obj.id_professional = professional
        super().save_model(request, obj, form, change)
        