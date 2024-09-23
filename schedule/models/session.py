from django.db import models
from django.utils.translation import gettext_lazy as _

class Session(models.Model):
    date = models.DateField(_("Data"), blank=False)
    LIST_STATUS = ( ('1', 'Agendado'), ('2', 'Em andamento'), ('3', 'Concluído'), ('4', 'Cancelado') )
    status = models.CharField(_("Status"), max_length=1, choices=LIST_STATUS, default='2', blank=False)
    id_package = models.ForeignKey(
        'schedule.Package'
        , on_delete=models.CASCADE
        , verbose_name='Pacote'
        , null=True
        , blank=True
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Sessão'
        verbose_name_plural = 'Sessões'
        ordering = ('date',)

    def __str__(self):
        return f''