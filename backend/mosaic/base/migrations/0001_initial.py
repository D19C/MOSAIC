# Generated by Django 4.2.5 on 2024-03-08 01:23

from django.db import migrations, models
import django_extensions.db.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Admin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(max_length=255, verbose_name='Nombre(s)')),
                ('last_name', models.CharField(max_length=255, verbose_name='Apellido(s)')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Fecha de Nacimiento')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Correo')),
                ('document_type', models.CharField(choices=[('C.C.', 'C.C.'), ('C.E.', 'C.E.'), ('Pasaporte', 'Pasaporte')], default='C.C.', max_length=255, verbose_name='Tipo de documento')),
                ('document', models.CharField(max_length=255, unique=True, verbose_name='Identificación')),
                ('address', models.CharField(max_length=255, verbose_name='Dirección')),
                ('cellphone', models.CharField(max_length=255, verbose_name='Celular')),
                ('gender', models.CharField(choices=[('masculino', 'Masculino'), ('femenino', 'Femenino'), ('otro', 'Otro')], default='Otro', max_length=255, verbose_name='Género')),
                ('status', models.CharField(choices=[('pending', 'Pendiente'), ('approved', 'Aprobado'), ('rejected', 'Rechazado')], default='pending', max_length=255, verbose_name='Estado')),
                ('token', models.IntegerField(blank=True, null=True, verbose_name='Token cambio de contraseña')),
                ('profile_image', models.FileField(blank=True, null=True, upload_to='user/profile_image', verbose_name='Imagen de perfil')),
            ],
            options={
                'verbose_name': 'Administrador',
                'verbose_name_plural': 'Administradores',
                'db_table': 'base_admin',
            },
        ),
        migrations.CreateModel(
            name='Auth',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creation_date', models.DateTimeField(auto_now_add=True)),
                ('is_disabled', models.BooleanField(default=False)),
                ('token', models.TextField(max_length=700, verbose_name='Token')),
            ],
            options={
                'verbose_name': 'Sesión',
                'verbose_name_plural': 'Sesiones',
                'db_table': 'base_auth',
            },
        ),
        migrations.CreateModel(
            name='Creator',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('username', models.CharField(max_length=50, unique=True, verbose_name='Username')),
            ],
            options={
                'verbose_name': 'Creador',
                'verbose_name_plural': 'Creadores',
                'db_table': 'base_creator',
            },
        ),
        migrations.CreateModel(
            name='EmailTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email_id', models.CharField(choices=[('client_register_confirmation', 'Confirmación de registro - Cliente'), ('admin_register_confirmation', 'Confirmación de registro - Administrador')], max_length=128, verbose_name='ID del correo')),
                ('subject', models.CharField(max_length=255, verbose_name='Asunto')),
                ('template', models.TextField(verbose_name='Plantilla')),
            ],
            options={
                'verbose_name': 'Plantilla de correo',
                'verbose_name_plural': 'Plantillas de correos',
                'db_table': 'base_email_template',
            },
        ),
        migrations.CreateModel(
            name='EmailTracking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified')),
                ('id_module', models.IntegerField(verbose_name='ID del módulo')),
                ('type_module', models.CharField(choices=[('cliente', 'Clientes'), ('administrador', 'Administradores')], default='cliente', max_length=255, verbose_name='Tipo del módulo')),
                ('subject', models.CharField(blank=True, max_length=255, null=True, verbose_name='Asunto')),
                ('receivers', models.CharField(max_length=255, verbose_name='Destinatarios')),
                ('content', models.TextField(blank=True, null=True, verbose_name='Contenido')),
                ('status', models.CharField(choices=[('sent', 'Enviado'), ('read', 'Leído'), ('error', 'Error al enviar')], default='sent', max_length=255, verbose_name='Estado del correo')),
                ('confirmation_token', models.CharField(max_length=255, verbose_name='Token de confirmación')),
            ],
            options={
                'verbose_name': 'Seguimiento de correo electrónico',
                'verbose_name_plural': 'Seguimientos de correos electrónicos',
                'db_table': 'base_email_tracking',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('first_name', models.CharField(max_length=255, verbose_name='Nombre(s)')),
                ('last_name', models.CharField(max_length=255, verbose_name='Apellido(s)')),
                ('birth_date', models.DateField(blank=True, null=True, verbose_name='Fecha de Nacimiento')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Correo')),
                ('document_type', models.CharField(choices=[('C.C.', 'C.C.'), ('C.E.', 'C.E.'), ('Pasaporte', 'Pasaporte')], default='C.C.', max_length=255, verbose_name='Tipo de documento')),
                ('document', models.CharField(max_length=255, unique=True, verbose_name='Identificación')),
                ('address', models.CharField(max_length=255, verbose_name='Dirección')),
                ('cellphone', models.CharField(max_length=255, verbose_name='Celular')),
                ('gender', models.CharField(choices=[('masculino', 'Masculino'), ('femenino', 'Femenino'), ('otro', 'Otro')], default='Otro', max_length=255, verbose_name='Género')),
                ('status', models.CharField(choices=[('pending', 'Pendiente'), ('approved', 'Aprobado'), ('rejected', 'Rechazado')], default='pending', max_length=255, verbose_name='Estado')),
                ('token', models.IntegerField(blank=True, null=True, verbose_name='Token cambio de contraseña')),
                ('profile_image', models.FileField(blank=True, null=True, upload_to='user/profile_image', verbose_name='Imagen de perfil')),
            ],
            options={
                'verbose_name': 'Usuario',
                'verbose_name_plural': 'Usuarios',
                'db_table': 'base_user',
            },
        ),
        migrations.CreateModel(
            name='EnvironmentVariables',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('var_name', models.CharField(max_length=255, verbose_name='Nombre de variable')),
                ('var_value', models.CharField(max_length=700, verbose_name='Valor')),
                ('var_type', models.CharField(choices=[('string', 'Cadena'), ('float', 'Decimal'), ('integer', 'Entero'), ('boolean', 'Booleano'), ('json', 'JSON')], max_length=15, verbose_name='Tipo de variable')),
                ('description', models.CharField(max_length=255, verbose_name='Descripción')),
            ],
            options={
                'verbose_name': 'Variable de entorno',
                'verbose_name_plural': 'Variables de entorno',
                'db_table': 'base_environment_variables',
                'indexes': [models.Index(fields=['var_name'], name='envs_var_name_idx')],
            },
        ),
        migrations.AddConstraint(
            model_name='environmentvariables',
            constraint=models.UniqueConstraint(fields=('var_name',), name='envs_uniqueness'),
        ),
        migrations.AddIndex(
            model_name='emailtemplate',
            index=models.Index(fields=['email_id'], name='email_id_idx'),
        ),
        migrations.AddConstraint(
            model_name='emailtemplate',
            constraint=models.UniqueConstraint(fields=('email_id',), name='email_id_uniqueness'),
        ),
        migrations.AddIndex(
            model_name='auth',
            index=models.Index(fields=['token'], name='auth_token_idx'),
        ),
    ]