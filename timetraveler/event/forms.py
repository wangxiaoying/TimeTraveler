from django import forms

class EventImagesForm(forms.Form):
	images = forms.FileField()