# Generated by Django 3.1.3 on 2021-01-06 11:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('G_neighbour', '0008_user_rating_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='user_rating',
            name='comment',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='user_rating',
            name='rating',
            field=models.PositiveSmallIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')]),
        ),
        migrations.DeleteModel(
            name='rating_page',
        ),
        migrations.DeleteModel(
            name='user_comment',
        ),
    ]