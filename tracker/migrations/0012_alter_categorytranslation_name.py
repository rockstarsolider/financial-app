# Generated by Django 5.1 on 2024-11-02 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0011_remove_category_name_categorytranslation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categorytranslation',
            name='name',
            field=models.CharField(max_length=15, unique=True, verbose_name='name'),
        ),
    ]
