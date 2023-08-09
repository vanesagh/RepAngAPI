# Generated by Django 4.2.3 on 2023-08-08 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('category', models.CharField(choices=[('pan', 'Pan'), ('pastel', 'Pastel'), ('galletas', 'Galletas'), ('pays', 'Pays')], max_length=10, null=True)),
            ],
        ),
    ]
