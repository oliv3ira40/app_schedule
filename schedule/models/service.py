from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=300, verbose_name='Nome')
    description = models.TextField(verbose_name='Descrição', null=True, blank=True)
    average_duration = models.TimeField(verbose_name='Duração Média (HH:MM:SS)', null=True, blank=True)
    average_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Preço Médio', null=True, blank=True)
    # image = models.ImageField(upload_to='services', verbose_name='Imagem', null=True, blank=True)
    id_professional = models.ForeignKey(
        'person.Professional'
        , on_delete=models.CASCADE
        , verbose_name='Profissional'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Data de Atualização')

    class Meta:
        verbose_name = 'Serviço'
        verbose_name_plural = 'Meus Serviços'

    def __str__(self):
        return self.name
    