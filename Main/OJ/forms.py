from dataclasses import field
from django import forms
from django.forms import ModelForm
from .models import Problems


class FileSubmission(ModelForm):
    class Meta:
        model = Problems
        fields = "__all__"