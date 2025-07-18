# Generated by Django 5.1.4 on 2025-06-23 03:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Reclamo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo_documento', models.CharField(choices=[('DNI', 'DNI'), ('CE', 'Carnet de extranjería'), ('PAS', 'Pasaporte'), ('OTRO', 'Otro')], max_length=10)),
                ('numero_documento', models.CharField(max_length=20)),
                ('nombres', models.CharField(max_length=100)),
                ('apellido_paterno', models.CharField(max_length=100)),
                ('apellido_materno', models.CharField(max_length=100)),
                ('departamento', models.CharField(max_length=100)),
                ('provincia', models.CharField(max_length=100)),
                ('distrito', models.CharField(max_length=100)),
                ('telefono_fijo', models.CharField(blank=True, max_length=15, null=True)),
                ('telefono_celular', models.CharField(max_length=15)),
                ('correo', models.EmailField(max_length=254)),
                ('identificacion', models.CharField(choices=[('PRODUCTO', 'Producto'), ('SERVICIO', 'Servicio')], max_length=20)),
                ('monto_reclamado', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('tienda', models.CharField(max_length=100)),
                ('fecha_compra', models.DateField(blank=True, null=True)),
                ('numero_boleta', models.CharField(blank=True, max_length=50, null=True)),
                ('numero_pedido', models.CharField(blank=True, max_length=50, null=True)),
                ('descripcion', models.TextField()),
                ('tipo', models.CharField(choices=[('RECLAMO', 'Reclamo'), ('QUEJA', 'Queja')], max_length=10)),
                ('detalle', models.TextField()),
                ('pedido_cliente', models.TextField()),
                ('fecha_envio', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
