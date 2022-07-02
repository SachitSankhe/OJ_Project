# Generated by Django 4.0.5 on 2022-06-29 10:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Problems',
            fields=[
                ('problem_id', models.BigAutoField(db_column='Problem ID', max_length=3, primary_key=True, serialize=False)),
                ('problem_name', models.CharField(db_column='Problem Name', max_length=50)),
                ('problem_statement', models.CharField(db_column='Problem Statement', max_length=400)),
                ('problem_code', models.CharField(db_column='Code', max_length=200)),
                ('problem_status', models.BooleanField(db_column='Solve_status', default=False)),
                ('problem_level', models.CharField(db_column='Problem level', max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fname', models.CharField(max_length=30, verbose_name='First Name')),
                ('sname', models.CharField(max_length=30, verbose_name='First Name')),
            ],
        ),
        migrations.CreateModel(
            name='TestCases',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('input', models.CharField(max_length=200, verbose_name='Input')),
                ('output', models.CharField(max_length=200, verbose_name='Output')),
                ('problem_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OJ.problems')),
            ],
        ),
        migrations.CreateModel(
            name='Solutions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('submitted_at', models.DateTimeField(verbose_name='Submitted on')),
                ('Verdict', models.CharField(max_length=20, verbose_name='Verdict')),
                ('problem_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='OJ.problems')),
            ],
        ),
    ]