from django import forms
from events.models import Game, Event

class GameForm(forms.ModelForm):
    class Meta:
        model = Game

class EventForm(forms.Form):
    game = forms.ModelChoiceField(queryset=Game.objects.all().order_by('name'), empty_label=None)
    start = forms.DateTimeField()
    end = forms.DateTimeField()
    min = forms.IntegerField()
    max = forms.IntegerField()
    
    def clean(self):
        cleaned_data = self.cleaned_data
        start = cleaned_data.get('start')
        end = cleaned_data.get('end')
        if start >= end:
            msg = u"End time must come after start time."
            self._errors['end'] = self.error_class([msg])
            del cleaned_data['end']
        min = cleaned_data.get('min')
        max = cleaned_data.get('max')
        if max < min:
            msg = u"Max may not be less than min."
            self._errors['max'] = self.error_class([msg])
            del cleaned_data['max']
        return cleaned_data