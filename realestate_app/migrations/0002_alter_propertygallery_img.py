# Generated by Django 5.0.3 on 2025-07-17 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realestate_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='propertygallery',
            name='img',
            field=models.ImageField(upload_to='imgs/'),
        ),
    ]
