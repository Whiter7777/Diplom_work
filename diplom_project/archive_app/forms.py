from django import forms

class UserForm(forms.Form):
    number = forms.IntegerField()


class FindSample(forms.Form):
    find_sample = forms.CharField(max_length=20)