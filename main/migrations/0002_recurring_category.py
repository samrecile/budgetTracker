# Generated by Django 4.0.2 on 2022-03-01 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='recurring',
            name='category',
            field=models.CharField(choices=[('Expense', 'Expense'), ('Income', 'Income')], default=None, max_length=50),
            preserve_default=False,
        ),
    ]