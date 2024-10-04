from django.db import models
from django.utils.translation import gettext_lazy as _
from person.models.professional import Professional
from person.models.client import Client
from schedule.models.service import Service
from django.utils import timezone

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
    date = models.DateTimeField(verbose_name='Data do atendimento', null=True, blank=True)
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

    def get_count_fin_treatments_by_prof(request):
        current_user = request.user
        if current_user.is_superuser: return {}

        professional = Professional.objects.get(id_user=current_user)
        if not professional: return {}

        finished_treatments = Treatment.objects.filter(
            id_professional=professional,
            status='2'
        ).count()

        return finished_treatments
    
    def get_count_unfin_treatments_by_prof(request):
        current_user = request.user
        if current_user.is_superuser: return {}

        professional = Professional.objects.get(id_user=current_user)
        if not professional: return {}

        unfinished_treatments = Treatment.objects.filter(
            id_professional=professional,
            status='1'
        ).count()

        return unfinished_treatments
    
    def get_next_treatments_by_prof(request):
        current_user = request.user
        if current_user.is_superuser: return {}

        professional = Professional.objects.get(id_user=current_user)
        if not professional: return {}

        next_treatments = Treatment.objects.filter(
            id_professional=professional,
            status='1'
        ).order_by('date')

        for treatment in next_treatments:
            treatment.client = Client.objects.get(id=treatment.id_client.id)
            treatment.service = Service.objects.get(id=treatment.id_service.id)
            treatment.type = 'Atendimento único'
            local_date = timezone.localtime(treatment.date)
            treatment.date = local_date.strftime('%d/%m/%Y %H:%M')

        return next_treatments