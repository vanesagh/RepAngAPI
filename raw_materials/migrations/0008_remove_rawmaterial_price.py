# Generated by Django 4.2.3 on 2023-07-25 23:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('raw_materials', '0007_alter_rawmaterial_price_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rawmaterial',
            name='price',
        ),
    ]
