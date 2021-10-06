from django import forms
from .models import Detection

# For New Detection
class DetectForm(forms.ModelForm):
    class Meta:
        model = Detection
        fields = ['fname', 'lname', 'email', 'age', 'gender', 'address', 'city', 'state', 'image']
        labels = {
            'fname':'First Name',
            'lname':'Last Name',
            'email':'Email Address',
            'age':'Age',
            'gender':'Gender',
            'address':'Address',
            'city':'City',
            'state':'State',
            'image':'Image'}
        widgets = {
            'fname': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'First Name'}),
            'lname': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Last Name'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Email'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder':'Age', 'min':18, 'max':100}),
            'gender': forms.Select(attrs={'class': 'form-control', 'placeholder':'Gender'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'City'}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'State'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'placeholder':'Image'})}

# For Update the Data
class UpdateForm(forms.ModelForm):
    class Meta:
        model = Detection
        fields = ['fname', 'lname', 'email', 'address', 'city', 'state']
        labels = {
            'fname':'First Name',
            'lname':'Last Name',
            'email':'Email Address',
            'address':'Address',
            'city':'City',
            'state':'State'}
        widgets = {
            'fname': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'First Name', 'editable':False}),
            'lname': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Last Name'}),
            'email': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Email'}),
            'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Address'}),
            'city': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'City', 'editable':False}),
            'state': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'State', 'editable':False})}