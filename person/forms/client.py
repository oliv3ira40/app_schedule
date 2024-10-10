from django import forms
from person.models import Client
from person.models.professional import Professional
from django.utils.translation import gettext_lazy as _

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        cpf = cleaned_data.get('cpf')
        email = cleaned_data.get('email')
        phone = cleaned_data.get('phone')
        professional = cleaned_data.get('id_professional')
        current_user = self.request.user
        if not current_user.is_superuser:
            professional = Professional.objects.get(id_user=current_user)

        # if not professional:
        #     raise forms.ValidationError('O campo profissional é obrigatório.')

        if self.instance.pk is None:  # Verificação durante a criação
            if cpf and Client.objects.filter(cpf=cpf, id_professional=professional).exists():
                raise forms.ValidationError(_('You cannot have two clients with the same CPF'))
            if email and Client.objects.filter(email=email, id_professional=professional).exists():
                raise forms.ValidationError(_('You cannot have two clients with the same E-mail'))
            if phone and Client.objects.filter(phone=phone, id_professional=professional).exists():
                raise forms.ValidationError(_('You cannot have two clients with the same Phone'))
        else:  # Verificação durante a edição
            if cpf and Client.objects.filter(cpf=cpf, id_professional=professional).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError(_('You cannot have two clients with the same CPF'))
            if email and Client.objects.filter(email=email, id_professional=professional).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError(_('You cannot have two clients with the same E-mail'))
            if phone and Client.objects.filter(phone=phone, id_professional=professional).exclude(pk=self.instance.pk).exists():
                raise forms.ValidationError(_('You cannot have two clients with the same Phone'))

        return cleaned_data
