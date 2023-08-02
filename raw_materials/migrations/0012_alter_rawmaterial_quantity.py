# Generated by Django 4.2.3 on 2023-07-27 01:26

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('raw_materials', '0011_alter_rawmaterial_quantity_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rawmaterial',
            name='quantity',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(1000)]),
        ),
    ]