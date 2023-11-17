from django import forms
from django.forms import inlineformset_factory

from partnership.models import FeedbackJob, Photo

PhotoFormSet = inlineformset_factory(FeedbackJob, Photo, fields=('photo',), extra=3)


class FeedbackJobForm(forms.ModelForm):
    """Заявка"""

    class Meta:
        model = FeedbackJob
        exclude = 'datetime_start', 'status', 'datetime_end', 'message_comment',
