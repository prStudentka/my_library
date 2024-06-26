# Generated by Django 4.1.6 on 2023-03-26 08:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mylibrary', '0010_alter_category_description_alter_comment_date_update'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='date_add',
        ),
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.CharField(max_length=30, null=True, verbose_name='Автор'),
        ),
        migrations.AlterField(
            model_name='category',
            name='description',
            field=models.TextField(blank=True, null=True, verbose_name='Описание'),
        ),
    ]
