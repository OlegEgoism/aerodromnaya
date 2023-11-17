from django import forms
from partnership.models import FeedbackJob, Photo
from django.forms import inlineformset_factory

PhotoFormSet = inlineformset_factory(FeedbackJob, Photo, fields=('photo',), extra=3)


class FeedbackJobForm(forms.ModelForm):
    """Заявка"""

    class Meta:
        model = FeedbackJob
        exclude = ('datetime_start', 'status', 'datetime_end', 'message_comment')
        widgets = {
            'last_name': forms.TextInput(attrs={'placeholder': 'Фамилия'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Имя'}),
            'middle_name': forms.TextInput(attrs={'placeholder': 'Отчество'}),
            'apartment': forms.TextInput(attrs={'placeholder': 'Квартира'}),
            'entrance': forms.TextInput(attrs={'placeholder': 'Подъезд'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Телефонный номер в формате: +37525... +37529... +37533... +37544... '}),
            'message': forms.Textarea(attrs={'placeholder': 'Опишите проблему полностью. При необходимости можете прикрепить фотографии в количестве 3 шт.', 'rows': 10})
        }
