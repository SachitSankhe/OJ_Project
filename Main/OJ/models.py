import datetime

from django.db import models
from django.utils import timezone
from django.core.validators import FileExtensionValidator
# Create your models here.


class User(models.Model):
    fname = models.CharField('First Name', max_length=30)
    sname = models.CharField('First Name', max_length=30)
    # User_totalscore = models.FloatField()
    def __str__(self):
        return self.fname


def content_file_name(instance, filename):
    return '/codeFiles/'.join([instance.problem.problem_id, filename])

class Problem(models.Model):
    problem_id = models.BigAutoField(
        primary_key=True, db_column="Problem ID")
    problem_name = models.CharField(max_length=50, db_column="Problem Name")
    problem_statement = models.CharField(
        max_length=400, db_column="Problem Statement")
    problem_status = models.BooleanField(
        db_column="Solve_status", default=False)
    problem_level = models.CharField(max_length=10, db_column="Problem level")
    # problem_maxscore = models.FloatField(db_column="Max Score")
    # problem_scored = models.FloatField(db_column="Scored")

    def __str__(self):
        return self.problem_name

    # def problem_directory_path(instance):
    #     return 'codefiles/problem_{0}'.format(instance.problem_id)



class TestCase(models.Model):
    problem_id = models.ForeignKey(Problem, on_delete=models.CASCADE)
    input = models.FileField('Input', max_length=200)
    output = models.CharField('Output', max_length=200)

    def __str__(self):
        return self.input


class Solution(models.Model):
    problem_id = models.ForeignKey(Problem, on_delete=models.CASCADE)
    problem_code = models.FileField(upload_to= "media",default=True ,validators=[FileExtensionValidator(allowed_extensions=['cpp'])])
    submitted_at = models.DateTimeField('Submitted on')
    Verdict = models.CharField('Verdict', max_length=20,blank=True)

    def __str__(self):
        return self.Verdict
