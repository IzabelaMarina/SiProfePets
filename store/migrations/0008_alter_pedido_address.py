# Generated by Django 4.0.3 on 2022-04-13 18:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0007_pedido_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='address',
            field=models.CharField(blank=True, default='', max_length=50, null=True),
        ),
    ]
