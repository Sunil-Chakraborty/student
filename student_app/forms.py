from django import forms
  
class PathForm(forms.Form):
    path_name = forms.CharField()
    path_field = forms.FileField()