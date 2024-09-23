# Generated by Django 4.2.1 on 2024-09-03 18:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('person', '0004_alter_client_cpf_alter_client_email_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Data de Criação'),
        ),
        migrations.AddField(
            model_name='client',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Data de Atualização'),
        ),
        migrations.AddField(
            model_name='professional',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True, verbose_name='Data de Criação'),
        ),
        migrations.AddField(
            model_name='professional',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Data de Atualização'),
        ),
    ]
