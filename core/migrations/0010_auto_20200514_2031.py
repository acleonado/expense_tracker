# Generated by Django 3.0.5 on 2020-05-14 20:31

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0009_auto_20200506_2220'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='budget',
            name='account',
        ),
        migrations.AddField(
            model_name='budget',
            name='username',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='accounttransaction',
            name='budget',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Budget'),
        ),
        migrations.AlterField(
            model_name='budgettransaction',
            name='budget',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='budgettransaction', to='core.Budget'),
        ),
    ]
