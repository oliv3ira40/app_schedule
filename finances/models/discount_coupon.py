from django.db import models
from django.core.validators import MinValueValidator
import string
import random

# Gera um código aleatório com letras e números
def generate_random_code(length=10):
    characters = string.ascii_lowercase + string.digits
    return ''.join(random.choices(characters, k=length))

class DiscountCoupon(models.Model):
    code = models.CharField(max_length=20, verbose_name='Código', default=generate_random_code, blank=False)
    TYPE_DISCOUNT = ( ('1', 'Valor de desconto'), ('2', 'Porcentagem de desconto') )
    type_discount = models.CharField(max_length=1, choices=TYPE_DISCOUNT, verbose_name='Tipo de Desconto', default='1', blank=False)
    discount_amount = models.DecimalField(max_digits=5, decimal_places=2, verbose_name='Valor do Desconto', null=True, blank=True)
    discount_percentage = models.IntegerField(verbose_name='Porcentagem de Desconto', null=True, blank=True)
    valid_days = models.IntegerField(
        verbose_name='Dias de Validade', null=True, blank=True
        , validators=[MinValueValidator(1)]
        , help_text='Prazo de validade do cupom em dias, deixe em branco para não expirar'
    )
    max_value_discount = models.DecimalField(
        max_digits=5, decimal_places=2, verbose_name='Valor Máximo do Desconto'
        , null=True, blank=True, default=20
    )
    used = models.BooleanField(verbose_name='Usado', default=False, help_text='Cupons usados não podem ser utilizados novamente')
    cancelled = models.BooleanField(verbose_name='Cupom encerrado', default=False, help_text='Cupons encerrados não podem ser utilizados')    
    id_professional = models.ForeignKey(
        'person.Professional'
        , verbose_name='Profissional'
        , on_delete=models.CASCADE
        , null=True
        , blank=True
    )
    specific_client = models.BooleanField(
        verbose_name='Redirecionar para Cliente Específico?'
        , default=False
        , help_text='Marque se este cupom for destinado a um cliente específico.'
    )
    id_client = models.ForeignKey(
        'person.Client'
        , verbose_name='Cliente Ganhador do Cupom'
        , on_delete=models.CASCADE
        , null=True
        , blank=True
        , help_text='O cliente poderá usar o cupom somente uma vez.'
    )
    coupon_usage_limit = models.PositiveIntegerField(
        verbose_name='Limite de Uso do Cupom',
        default=1,
        help_text='Número máximo de vezes que o cupom pode ser utilizado, uma vez por cliente.'
    )

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Data de Atualização', null=True, blank=True)

    def __str__(self):
        return self.code
    
    class Meta:
        verbose_name = 'Cupom de Desconto'
        verbose_name_plural = 'Cupons de Desconto'
