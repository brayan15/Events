from django import forms
from .models import Event

class EventForm(forms.ModelForm):
	class Meta:
		model = Event
		fields = ('name','description','content','category','city','place','date','start','end','image','free','price',)
		widgets = {
		'name':forms.TextInput(attrs={'class':'form-control','placeholder': 'Name'}),
		'description':forms.Textarea(attrs={'class':'form-control','placeholder': 'Enter a description of event'}),
		'content':forms.Textarea(attrs={'class':'form-control','placeholder': 'Enter the topic of event'}),
		'city':forms.TextInput(attrs={'class':'form-control','placeholder': 'City'}),
		'place':forms.TextInput(attrs={'class':'form-control','placeholder': 'Place'}),
		'date':forms.DateInput(attrs={'class':'form-control date-picker','placeholder': 'Date'}),
		'start':forms.DateInput(attrs={'class':'form-control date-time','placeholder': 'Time start'}),
		'end':forms.DateInput(attrs={'class':'form-control date-time','placeholder': 'Time end'}),
		'image':forms.ClearableFileInput(attrs={'class':'form-control'}),
		'free':forms.CheckboxInput(attrs={'class':'form-control'}),
		'price':forms.NumberInput(attrs={'class':'form-control','placeholder': 'Price'})
		}