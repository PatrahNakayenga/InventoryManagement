# Generated by Django 5.1.5 on 2025-01-30 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0004_issueout_quantity_alter_issueout_inventoryitem'),
    ]

    operations = [
        migrations.AlterField(
            model_name='issueout',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]
