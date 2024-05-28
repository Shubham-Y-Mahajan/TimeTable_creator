from django import forms

class ApplicationForm(forms.Form):
    FirstName = forms.CharField(max_length=80)
    LastName = forms.CharField(max_length=80)
    Email = forms.EmailField()
    Date = forms.DateField()
    occupation = forms.CharField(max_length=80)

    #note index.html 'name' field , the names here and in views.py should match