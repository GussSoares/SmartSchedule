# Generated by Django 3.0.8 on 2020-07-29 21:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Modificado em')),
                ('login', models.CharField(max_length=50, unique=True, verbose_name='Login')),
                ('first_name', models.CharField(max_length=50, verbose_name='Primeiro Nome')),
                ('last_name', models.CharField(blank=True, max_length=50, null=True, verbose_name='Último Nome')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Email')),
                ('cpf_cnpj', models.CharField(blank=True, max_length=14, null=True, verbose_name='CPF/CNPJ')),
                ('telefone', models.CharField(blank=True, max_length=13, null=True, verbose_name='Telefone')),
                ('is_active', models.BooleanField(default=True, verbose_name='Ativo')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'db_table': 'cliente',
            },
        ),
    ]
