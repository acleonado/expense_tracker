# Generated by Django 3.0.5 on 2020-05-05 21:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0006_auto_20200505_1955'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accounttransaction',
            name='budget',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Budget'),
        ),
        migrations.AlterField(
            model_name='accounttransaction',
            name='trans_type',
            field=models.CharField(max_length=15),
        ),
    ]
