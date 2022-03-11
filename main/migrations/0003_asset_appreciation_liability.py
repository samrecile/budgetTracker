# Generated by Django 4.0.2 on 2022-03-10 22:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0002_recurring_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='asset',
            name='appreciation',
            field=models.DecimalField(blank=True, decimal_places=2, default=0, max_digits=8),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name='liability',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('value', models.DecimalField(decimal_places=2, max_digits=8)),
                ('interest', models.DecimalField(decimal_places=2, max_digits=8)),
                ('payment', models.DecimalField(decimal_places=2, max_digits=8)),
                ('date_added', models.DateField(auto_now_add=True)),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]