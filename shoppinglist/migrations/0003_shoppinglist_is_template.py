# Generated by Django 2.2.2 on 2019-06-22 23:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shoppinglist', '0002_shoppingitem_done'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppinglist',
            name='is_template',
            field=models.BooleanField(default=False, verbose_name='template'),
        ),
    ]
