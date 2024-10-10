from django.db import models
from django.utils.translation import gettext_lazy as _
from person.models.professional import Professional

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
        verbose_name_plural = 'Pacotes de atendimentos'
        ordering = ('created_at',)

    def __str__(self):
        return f'{self.id_service} do cliente {self.id_client}'

    def get_count_fin_packages_by_prof(request):
        current_user = request.user
        if current_user.is_superuser: return {}

        professional = Professional.objects.get(id_user=current_user)
        if not professional: return {}

        finished_packages = Package.objects.filter(
            id_professional=professional,
            closed=True
        ).count()

        return finished_packages
    
    def get_count_unfin_packages_by_prof(request):
        current_user = request.user
        if current_user.is_superuser: return {}

        professional = Professional.objects.get(id_user=current_user)
        if not professional: return {}

        unfinished_packages = Package.objects.filter(
            id_professional=professional,
            closed=False
        ).count()

        return unfinished_packages
