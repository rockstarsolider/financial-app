# Generated by Django 5.1 on 2024-08-31 20:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0005_alter_transaction_date_alter_transaction_type'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='transaction',
            options={'ordering': ['-date']},
        ),
        migrations.AlterField(
            model_name='transaction',
            name='date',
            field=models.DateField(),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='type',
            field=models.CharField(choices=[('income', 'درآمد'), ('expense', 'هزینه')], max_length=8),
        ),
    ]
