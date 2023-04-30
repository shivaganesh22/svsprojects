from .models import *
from django import forms
from django.forms.models import inlineformset_factory

class VideoForm(forms.ModelForm):
    class Meta:
        model=Video
        fields='__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
    def clean_title(self):
        n=self.cleaned_data.get('title')
        return n.title()
    def clean_hidden_title(self):
        n=self.cleaned_data.get('hidden_title')
        return n.title()

class QuizForm(forms.ModelForm):
    class Meta:
        model=Quizs
        fields='__all__'
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
    
