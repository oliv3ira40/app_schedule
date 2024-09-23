# Generated by Django 4.2.1 on 2024-09-03 20:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0004_package_alter_service_average_duration_treatment_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='package',
            options={'ordering': ('created_at',), 'verbose_name': 'Pacote', 'verbose_name_plural': 'Pacotes'},
        ),
        migrations.AlterModelOptions(
            name='treatment',
            options={'ordering': ('created_at',), 'verbose_name': 'Atendimento', 'verbose_name_plural': 'Atendimentos'},
        ),
        migrations.AddField(
            model_name='treatment',
            name='date',
            field=models.DateField(blank=True, null=True, verbose_name='Data'),
        ),
        migrations.AlterField(
            model_name='treatment',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Criado em'),
        ),
        migrations.AlterField(
            model_name='treatment',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='Atualizado em'),
        ),
    ]
