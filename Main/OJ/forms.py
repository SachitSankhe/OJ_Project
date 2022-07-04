from dataclasses import field
from django import forms
from django.forms import ModelForm
from .models import Solution


class FileSubmission(ModelForm):
    class Meta:
        model = Solution
        fields = ["problem_code","submitted_at"]