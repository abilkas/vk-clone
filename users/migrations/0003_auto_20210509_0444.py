# Generated by Django 3.1.6 on 2021-05-08 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_userfollowing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='birth_date',
            field=models.DateField(blank=True, null=True, verbose_name='День рождения'),
        ),
    ]