from django.db import models
from django.utils.translation import gettext_lazy as _

class Treatment(models.Model):
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
    date = models.DateField(verbose_name='Data do atendimento', null=True, blank=True)
    LIST_STATUS = ( ('1', 'Agendado'), ('2', 'Concluído'), ('3', 'Cancelado') )
    status = models.CharField(_("Status"), max_length=1, choices=LIST_STATUS, default='1', blank=False)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Criado em')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Atualizado em')
    
    class Meta:
        verbose_name = 'Atendimento'
        verbose_name_plural = 'Lista de Atendimentos'
        ordering = ('created_at',)

    def __str__(self):
        return self.id_service.name + ' do cliente ' + self.id_client.name
