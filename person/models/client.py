from django.db import models

class Client(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nome')
    email = models.EmailField(max_length=100, verbose_name='E-mail', null=True, blank=True)
    cpf = models.CharField(max_length=11, verbose_name='CPF', null=True, blank=True)
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
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Data de Atualização', null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
