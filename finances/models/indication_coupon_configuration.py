from django.db import models
from django.core.validators import MinValueValidator

class IndicationCouponConfiguration(models.Model):
    enable_indication_coupon = models.BooleanField(verbose_name='Habilitar Cupom de Indicação', default=False)
    
    TYPE_DISCOUNT = ( ('1', 'Valor de desconto'), ('2', 'Porcentagem de desconto') )
    type_discount = models.CharField(max_length=1, choices=TYPE_DISCOUNT, verbose_name='Tipo de Desconto', default='1', blank=False)
    discount_amount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Valor do Desconto', null=True, blank=True)
    discount_percentage = models.IntegerField(verbose_name='Porcentagem de Desconto', null=True, blank=True)
    
    valid_days = models.IntegerField(verbose_name='Dias de Validade', validators=[MinValueValidator(1)], null=True, blank=True, help_text='Prazo de validade do cupom em dias, deixe em branco para não expirar')
    max_value_discount = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name='Valor Máximo do Desconto'
        , null=True, blank=True, default=20, help_text='Valor máximo do desconto permitido'
    )
    
    id_professional = models.ForeignKey(
        'person.Professional'
        , verbose_name='Profissional'
        , on_delete=models.CASCADE
        , null=True
        , blank=True
    )
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Data de Atualização', null=True, blank=True)

    def __str__(self):
        return f'{self.id_professional}'
    
    class Meta:
        verbose_name = 'Config. do Cupom por Indicação'
        verbose_name_plural = 'Config. dos Cupons por Indicação'
