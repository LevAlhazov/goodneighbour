# Generated by Django 3.1.3 on 2021-01-06 12:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('G_neighbour', '0009_auto_20210106_1310'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_rating',
            name='comment',
            field=models.TextField(max_length=255),
        ),
    ]
