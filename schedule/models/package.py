from django.db import models
from django.utils.translation import gettext_lazy as _

class Package(models.Model):
    id_client = models.ForeignKey(
        'person.Client'
        , on_delete=models.CASCADE
        , verbose_name='Cliente'
    )
    id_professional = models.ForeignKey(
        'person.Professional'
        , on_delete=models.CASCADE
        , verbose_name='Profissional'
    )
    id_service = models.ForeignKey(
        'schedule.Service'
        , on_delete=models.CASCADE
        , verbose_name='Serviço'
    )

    value = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor', null=True, blank=True)
    description = models.TextField(_("Descrição"), null=True, blank=True)
    closed = models.BooleanField(_("Pacote concluído"), default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Pacote'
        verbose_name_plural = 'Lista de Pacotes'
        ordering = ('created_at',)

    def __str__(self):
        return f'{self.id_service} do cliente {self.id_client}'
