# Generated by Django 3.0.8 on 2020-09-03 00:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cliente', '0003_cliente_data_nascimento'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='foto',
            field=models.ImageField(blank=True, null=True, upload_to='', verbose_name='Foto de Perfil'),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='is_active',
            field=models.BooleanField(blank=True, default=True, verbose_name='Ativo'),
        ),
    ]