from django import forms


class LogInForm(forms.Form):
    name = forms.CharField(max_length=50)