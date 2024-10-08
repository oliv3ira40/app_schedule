from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from person.models import Client, Professional
from finances.models import DiscountCoupon, IndicationCouponConfiguration
from unfold.admin import ModelAdmin
from django.core.exceptions import ValidationError

@admin.register(Client)
class CustomClientAdmin(ModelAdmin):
    list_display = ('name', 'email', 'cpf', 'phone', 'birth_date', 'id_user', 'id_professional', 'id_indicator_by')
    search_fields = ('name', 'email', 'cpf', 'phone')
    ordering = ('name',)

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        # Se o usuário não for superusuário, remover os campos 'id_professional' e 'id_user'
        if not request.user.is_superuser:
            if 'id_professional' in form.base_fields:
                del form.base_fields['id_professional']
            if 'id_user' in form.base_fields:
                del form.base_fields['id_user']

            try:
                # Obtem o profissional atual
                professional = Professional.objects.get(id_user=request.user)
                
                # O erro é por conta disso
                # Filtrar os clientes do profissional atual
                queryset = Client.objects.filter(id_professional=professional)
                if obj:  # Se estiver editando, excluir o próprio cliente da lista de indicados
                    queryset = queryset.exclude(id=obj.id)
                
                form.base_fields['id_indicator_by'].queryset = queryset
            except Professional.DoesNotExist:
                # Se o profissional não existir, deixar o queryset de 'id_indicator_by' vazio
                form.base_fields['id_indicator_by'].queryset = Client.objects.none()

        return form

    def save_model(self, request, obj, form, change):
        # Previne a alteração do campo via código no backend (além da interface)
        if obj.pk:
            original = Client.objects.get(pk=obj.pk)
            if original.id_indicator_by and original.id_indicator_by != obj.id_indicator_by:
                raise ValidationError("O campo 'Indicado(a) por' não pode ser alterado após ser definido.")
        
        super().save_model(request, obj, form, change)

    # Adiciona o usuário ao get_form
    def get_form_kwargs(self, request, obj=None, **kwargs):
        form_kwargs = super().get_form_kwargs(request, obj, **kwargs)
        form_kwargs['user'] = request.user
        return form_kwargs

    def get_list_display(self, request):
        # Se o usuário não for superusuário, removemos 'id_professional' de list_display
        if not request.user.is_superuser:
            return ('name', 'email', 'cpf', 'phone', 'birth_date', 'id_indicator_by')
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

        # # Verificar se 'id_indicator_by' e 'id_professional' estão preenchidos
        # if obj.id_indicator_by and obj.id_professional:
        #     # Tentar obter a configuração de cupom para o profissional
        #     try:
        #         coupon_config = IndicationCouponConfiguration.objects.get(id_professional=obj.id_professional)

        #         # Criar o cupom de desconto baseado na configuração
        #         DiscountCoupon.objects.create(
        #             id_client=obj.id_indicator_by,  # Cliente que indicou
        #             id_professional=obj.id_professional,  # Profissional que gerou o cupom
        #             type_discount=coupon_config.type_discount,
        #             discount_amount=coupon_config.discount_amount,
        #             discount_percentage=coupon_config.discount_percentage,
        #             valid_days=coupon_config.valid_days,
        #             max_value_discount=coupon_config.max_value_discount,
        #         )
        #     except IndicationCouponConfiguration.DoesNotExist:
        #         # Tratar o caso onde não existe uma configuração de cupom
        #         self.message_user(request, "Configuração de cupom de indicação não encontrada para o profissional.", level="warning")
        
        super().save_model(request, obj, form, change)
