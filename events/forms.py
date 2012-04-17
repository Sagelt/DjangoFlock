from django import forms
from events.models import Publisher, Game, Event, Convention, Demand

class PublisherForm(forms.ModelForm):
    class Meta:
        model = Publisher
        #fields = ('name', 'publisher_url')

class GameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ('name', 'publisher', 'edition')

class ConventionForm(forms.ModelForm):
    class Meta:
        model = Convention
        fields = ('name', )

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ('convention', 'game', 'start', 'end', 'min', 'max')
    
    def clean(self):
        cleaned_data = self.cleaned_data
        start = cleaned_data.get('start')
        end = cleaned_data.get('end')
        if start >= end:
            msg = u"End time must come after start time."
            self._errors['end'] = self.error_class([msg])
            if 'end' in cleaned_data:
                del cleaned_data['end']
        min = cleaned_data.get('min')
        max = cleaned_data.get('max')
        if max < min:
            msg = u"Max may not be less than min."
            self._errors['max'] = self.error_class([msg])
            if 'max' in cleaned_data:
                del cleaned_data['max']
        return cleaned_data

class DemandForm(forms.ModelForm):
    class Meta:
        model = Demand
        fields = ('game', 'start', 'end')