from django import forms
from .models import TutoringHour

class TutoringHourForm(forms.ModelForm):
    class Meta:
        model = TutoringHour
        fields = ["day", "start_time", "end_time"]

    def clean(self):
        cleaned_data = super().clean()

        start_time = cleaned_data.get("start_time")
        end_time = cleaned_data.get("end_time")

        if start_time and end_time:
            if end_time <= start_time:
                raise forms.ValidationError(
                    "End time must be later than start time."
                )
            return cleaned_data
        