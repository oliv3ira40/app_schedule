# Generated by Django 4.2.1 on 2024-09-03 20:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0005_alter_package_options_alter_treatment_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='treatment',
            name='status',
            field=models.CharField(choices=[('1', 'Agendado'), ('2', 'Em andamento'), ('3', 'Concluído'), ('4', 'Cancelado'), ('5', 'Faltou')], default='2', max_length=1, verbose_name='Status'),
        ),
    ]
