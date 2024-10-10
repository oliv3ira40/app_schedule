from django.db import models
from datetime import date, timedelta
from django.utils import formats
from django.http import request
from person.models.professional import Professional
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class Client(models.Model):
    name = models.CharField(max_length=300, verbose_name='Nome')
    email = models.EmailField(max_length=100, verbose_name='E-mail', null=True, blank=True)
    cpf = models.CharField(max_length=20, verbose_name='CPF', null=True, blank=True)
    phone = models.CharField(max_length=20, verbose_name='Telefone', null=True, blank=True)
    birth_date = models.DateField(verbose_name='Data de Nascimento', null=True, blank=True)
    # photograph = models.ImageField(_("photograph"), upload_to="photos/")
    id_user = models.ForeignKey(
        'auth.User'
        , verbose_name='Usuário'
        , on_delete=models.CASCADE
        , null=True
        , blank=True
    )
    id_professional = models.ForeignKey(
        'Professional'
        , verbose_name='Profissional'
        , on_delete=models.CASCADE
        , null=True
        , blank=True
    )
    id_indicator_by = models.ForeignKey(
        'self'
        , verbose_name='Indicado(a) por'
        , on_delete=models.CASCADE
        , null=True
        , blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Data de Atualização', null=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        constraints = [
            models.UniqueConstraint(fields=['cpf', 'id_professional'], name='unique_cpf_by_professional'),
            models.UniqueConstraint(fields=['email', 'id_professional'], name='unique_email_by_professional'),
            models.UniqueConstraint(fields=['phone', 'id_professional'], name='unique_phone_by_professional')
        ]

    # Retorna os próximos aniversariantes dentro de um período de dias
    def get_upcoming_birthdays(request):
        current_user = request.user
        if current_user.is_superuser: return {}
        
        professional = Professional.objects.get(id_user=current_user)
        if not professional: return {}

        # Data de hoje e limite de dias para buscar próximos aniversários
        today = date.today()
        days_ahead = 30  # Define quantos dias à frente você quer buscar os aniversariantes
        date_limit = today + timedelta(days=days_ahead)
        current_year = today.year
        
        # Buscar os aniversariantes dentro do período especificado
        upcoming_birthdays = Client.objects.filter(
            birth_date__month__gte=today.month,
            birth_date__month__lte=date_limit.month,
            id_professional=professional
        ).order_by('birth_date')

        for client in upcoming_birthdays:
            client.age_at_next_birthday = current_year - client.birth_date.year
            
            client.phone = client.phone if client.phone else '---'
            if client.birth_date:
                client.formt_birth_date = f'{client.birth_date.day} de {formats.date_format(client.birth_date, "F")} de {current_year}'
            else:
                client.formt_birth_date = '---'
                client.age_at_next_birthday = '---'

        return upcoming_birthdays

    def get_count_clients_by_professional(request):
        current_user = request.user
        if current_user.is_superuser: return 0
        
        professional = Professional.objects.get(id_user=current_user)
        if not professional: return 0

        return Client.objects.filter(id_professional=professional).count()