from django.db import models
from django.utils.translation import gettext_lazy as _
from schedule.models import Package, Service
from django.utils import timezone

class Session(models.Model):
    date = models.DateTimeField(_("Data"), blank=False)
    description = models.TextField(_("Descrição"), blank=True)
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
        local_date = timezone.localtime(self.date)  # Converte para o fuso horário local
        format_date = local_date.strftime('%d/%m/%Y %H:%M')
        return f'Sessão do dia {format_date}'
    
    def get_scheduled_sessions():
        scheduled_sessions = Session.objects.filter(status='1').order_by('date')
        for session in scheduled_sessions[:]:
            session.package = Package.objects.get(id=session.id_package.id)
            if session.package.closed:
                scheduled_sessions.remove(session)
                continue
            
            session.service = Service.objects.get(id=session.package.id_service.id)

        return scheduled_sessions
