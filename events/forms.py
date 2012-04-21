from django import forms
from django.contrib.auth.models import User
from events.models import Publisher, Game, Event, Convention, Demand, UserProfile

class UserForm(forms.Form):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField(required=False)
    active_convention = forms.ModelChoiceField(Convention.objects.all(),
                                               empty_label="None",
                                               required=False)
    # @todo: make a value of u'' or None set active_convention to None, but a
    # missing active_convention key not change it. Currently, if you don't
    # specify the active_convention with each form submission, it nukes the
    # active convention.

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