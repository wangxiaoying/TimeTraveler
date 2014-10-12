from django import forms

class PortraitForm(forms.Form):
	portrait = forms.FileField()
