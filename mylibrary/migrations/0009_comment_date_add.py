# Generated by Django 4.1.6 on 2023-03-26 08:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mylibrary', '0008_alter_book_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='date_add',
            field=models.DateTimeField(auto_now=True, null=True, verbose_name='Дата обновления'),
        ),
    ]