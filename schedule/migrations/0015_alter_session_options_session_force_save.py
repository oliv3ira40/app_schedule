# Generated by Django 4.2.16 on 2024-10-05 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0014_alter_session_date_alter_session_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='session',
            options={'ordering': ('-date',), 'verbose_name': 'Sessão', 'verbose_name_plural': 'Sessões'},
        ),
        migrations.AddField(
            model_name='session',
            name='force_save',
            field=models.BooleanField(default=True, editable=False),
        ),
    ]
