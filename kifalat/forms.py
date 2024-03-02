# forms.py
from django import forms
from .models import Progress

class ProgressForm(forms.ModelForm):
    class Meta:
        model = Progress
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Dynamically adjust the queryset for the 'student' field based on the selected 'kafeel'
        if 'kafeel' in self.data:
            kafeel_id = int(self.data.get('kafeel'))
            self.fields['student'].queryset = self.fields['student'].queryset.filter(kafeel_id=kafeel_id)
        elif self.instance and self.instance.pk:
            # If editing an existing instance, set the queryset based on the current 'kafeel'
            self.fields['student'].queryset = self.fields['student'].queryset.filter(kafeel=self.instance.kafeel)
