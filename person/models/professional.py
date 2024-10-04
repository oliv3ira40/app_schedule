from django.db import models

class Professional(models.Model):
    name = models.CharField(max_length=200, verbose_name='Nome')
    email = models.EmailField(max_length=100, unique=True, verbose_name='E-mail', null=True, blank=True)
    cpf = models.CharField(max_length=11, unique=True, verbose_name='CPF', null=True, blank=True)
    phone = models.CharField(max_length=20, unique=True, verbose_name='Telefone (WhatsApp)', null=True, blank=True)
    # photograph = models.ImageField(_("photograph"), upload_to="photos/")
    id_user = models.ForeignKey(
        'auth.User'
        , verbose_name='Usuário'
        , on_delete=models.CASCADE
        , null=True
        , blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Data de Criação', null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Data de Atualização', null=True, blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Profissional'
        verbose_name_plural = 'Perfil Profissional'
