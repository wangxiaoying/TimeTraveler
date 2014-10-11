from django import forms

class TimeCapsuleForm(forms.Form):
	capsule = forms.FileField()