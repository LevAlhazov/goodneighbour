# Generated by Django 3.1.3 on 2021-01-06 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('G_neighbour', '0011_private_message'),
    ]

    operations = [
        migrations.AddField(
            model_name='private_message',
            name='title',
            field=models.CharField(default=True, max_length=150),
        ),
    ]