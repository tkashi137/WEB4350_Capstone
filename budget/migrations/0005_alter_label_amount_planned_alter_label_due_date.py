# Generated by Django 4.1.2 on 2022-10-22 22:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('budget', '0004_alter_label_amount_received_alter_label_notes_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='label',
            name='amount_planned',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=7, null=True),
        ),
        migrations.AlterField(
            model_name='label',
            name='due_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
