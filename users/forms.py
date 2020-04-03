from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django import forms

from .widgets import FengyuanChenDatePickerInput
from users.models import Person, Athlete, Coach

import re

class PersonCreationForm(UserCreationForm):

    class Meta:
        model = Person
        fields=('name', 'last_name', 'email', 'password1', 'password2')
        help_texts = {'email': ('confirmation link will be sent to this address'),}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].required = False
        self.fields['last_name'].required = False
        self.fields['password1'].help_text = None
    
class PersonChangeForm(UserChangeForm):

    class Meta:
        model = Person
        exclude = ['code']

class CoachRegisterForm(ModelForm):
    class Meta:
        model = Coach
        fields = '__all__'
        help_texts = {'age': ('Please enter your age here'),
                                'salary': ('Please enter your salary here.'),
                                'start_time': ('Work hour starting time'),
                                'end_time': ('Work hour ending time'),
                                'user': ('Who are you? Or better to say by which person are you?')}
        
        error_messages = {'start_time': {'invalid': 'Enter time in a correct format HH:mm:ss for instance:\
                                                                    18:00:00'},
                                          'end_time': {'invalid': 'Enter time in a correct format HH:mm:ss for instance:\
                                                                    19:30:00'}}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['age'].widget.attrs['min'] = 10
        self.fields['age'].widget.attrs['max'] = 100

class AthleteRegisterForm(ModelForm):
    class Meta:
        model = Athlete
        fields = '__all__'
        widgets =  {
            'last_payment': FengyuanChenDatePickerInput(), # datepicker pop up
        }

        help_texts = {'age': ('Please enter your age here'),
                                'start_time': ('Training starting time'),
                                'end_time': ('Training ending time'),
                                'user': ('Who are you? Or better to say by which person are you?'),
                                'trainer': ('Which coach do you want to work with')}

        error_messages = {'start_time': {'invalid': 'Enter time in a correct format HH:mm:ss for instance:\
                                                                    18:00:00'},
                                          'end_time': {'invalid': 'Enter time in a correct format HH:mm:ss for instance:\
                                                                    19:30:00'}}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['age'].widget.attrs['min'] = 10
        self.fields['age'].widget.attrs['max'] = 100
        self.fields['last_payment'].required = True
        self.fields['trainer'].required = False
        self.fields['start_time'].required = False
        self.fields['end_time'].required = False
    
    def clean_sport_field(self):
        sport_field = self.cleaned_data.get('sport_field')
        coach = Coach.objects.get(pk=int(self.data['trainer']))
        if coach.sport_field != sport_field:
            raise ValidationError(f'Your sport field and your coach sport field must be the same. Your\
                coach sport field is {coach.sport_field}')
        return sport_field

    def clean_days_of_week(self):
        days_of_week = set(self.cleaned_data.get('days_of_week'))
        coach = Coach.objects.get(pk=int(self.data['trainer']))
        coach_days_of_week = set(coach.days_of_week.all())
        print(days_of_week not in coach_days_of_week)
        if days_of_week != coach_days_of_week:
            raise ValidationError('Your coach goes to gym in different days')
        return days_of_week

    def clean_start_time(self):
        start_time = self.cleaned_data.get('start_time')
        coach = Coach.objects.get(pk=int(self.data['trainer']))
        if start_time < coach.start_time:
            raise ValidationError(f'Your coach arrives at the gym later than this time. He or She arrives at\
                                                    {coach.start_time}')
        return start_time

    def clean_end_time(self):
        end_time = self.cleaned_data.get('end_time')
        coach = Coach.objects.get(pk=int(self.data['trainer']))
        if end_time > coach.end_time:
            raise ValidationError(f'Your coach leaves the gym sooner than this time. He or She arrives at\
                                                    {coach.end_time}')
        return end_time