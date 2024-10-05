# forms.py

from django import forms
from .models import Project, Collaboration, CodeSnippet

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description']

class CollaborationForm(forms.ModelForm):
    class Meta:
        model = Collaboration
        fields = []



class CodeSnippetForm(forms.ModelForm):
    class Meta:
        model = CodeSnippet
        fields = ['code']

