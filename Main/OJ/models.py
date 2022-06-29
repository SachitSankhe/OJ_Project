import datetime

from django.db import models
from django.utils import timezone
# Create your models here.


class User(models.Model):
    fname = models.CharField('First Name', max_length=30)
    sname = models.CharField('First Name', max_length=30)

    # User_totalscore = models.FloatField()
    def __str__(self):
        return self.fname


class Problems(models.Model):
    problem_id = models.BigAutoField(
        primary_key=True, db_column="Problem ID")
    problem_name = models.CharField(max_length=50, db_column="Problem Name")
    problem_statement = models.CharField(
        max_length=400, db_column="Problem Statement")
    problem_code = models.CharField(max_length=200, db_column="Code")
    problem_status = models.BooleanField(
        db_column="Solve_status", default=False)
    problem_level = models.CharField(max_length=10, db_column="Problem level")
    # problem_maxscore = models.FloatField(db_column="Max Score")
    # problem_scored = models.FloatField(db_column="Scored")

    def __str__(self):
        return self.problem_name


class TestCases(models.Model):
    problem_id = models.ForeignKey(Problems, on_delete=models.CASCADE)
    input = models.FileField('Input', max_length=200)
    output = models.CharField('Output', max_length=200)

    def __str__(self):
        return self.input


class Solutions(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE)
    problem_id = models.ForeignKey(Problems, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField('Submitted on')
    Verdict = models.CharField('Verdict', max_length=20)

    def __str__(self):
        return self.Verdict
