# Generated by Django 4.0.5 on 2022-07-11 07:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('OJ', '0002_rename_user_id_solution_user'),
    ]

    operations = [
        migrations.AlterField(
            model_name='testcase',
            name='input',
            field=models.CharField(max_length=200, verbose_name='Input'),
        ),
    ]