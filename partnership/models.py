import re
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone


def phone_validator(phone_number):
    regular = r'(\+375)?(?:33|44|25|29)?([0-9]{7})'
    if re.fullmatch(regular, phone_number):
        return phone_number
    else:
        raise ValidationError('Неправильный номер телефона')


class InfoChairman(models.Model):
    """Контакты председателя"""
    fio = models.CharField(verbose_name='ФИО', max_length=200)
    phone = models.CharField(verbose_name='Мобильный телефон', max_length=20, validators=[phone_validator])
    time_start = models.CharField(verbose_name='Время начала работы', max_length=7)
    time_end = models.CharField(verbose_name='Время окончания работы', max_length=7)

    class Meta:
        verbose_name = 'Контакты'
        verbose_name_plural = 'Контакты'

    def __str__(self):
        return self.fio


class FeedbackJob(models.Model):
    """Заявка"""
    STATUS_CHOICES = [
        ('-', '-'),
        ('В работе', 'В работе'),
        ('Выполнен', 'Выполнен'),
    ]
    last_name = models.CharField(verbose_name='Фамилия', max_length=100)
    first_name = models.CharField(verbose_name='Имя', max_length=100)
    middle_name = models.CharField(verbose_name='Отчество', max_length=100)
    apartment = models.IntegerField(verbose_name='Квартира', validators=[MinValueValidator(1), MaxValueValidator(650)])
    entrance = models.IntegerField(verbose_name='Подъезд', validators=[MinValueValidator(1), MaxValueValidator(9)])
    phone = models.CharField(verbose_name='Телефон', max_length=20, validators=[phone_validator], help_text='телефон в формате +37525....... +37529....... +37533....... +37544.......')
    message = models.TextField(verbose_name='Сообщение')
    status = models.CharField(verbose_name='Статус', max_length=10, choices=STATUS_CHOICES, default='-')
    datetime_start = models.DateTimeField(verbose_name='Дата заявки', auto_now=True)
    datetime_end = models.DateField(verbose_name='Дата закрытия заявки', null=True, blank=True)
    message_comment = models.TextField(verbose_name='Ответ от председателя', null=True, blank=True)

    class Meta:
        verbose_name = 'Заявки'
        verbose_name_plural = 'Заявки'
        ordering = '-datetime_start',

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'

    def save(self, *args, **kwargs):
        if self.status == 'Выполнен' and not self.datetime_end:
            self.datetime_end = timezone.now().date()
        elif self.status != 'Выполнен':
            self.datetime_end = None  # Сбрасываем дату, если статус не "Выполнен"
        super().save(*args, **kwargs)

class Photo(models.Model):
    """Фотография"""
    photo = models.ImageField(verbose_name='Фотография', upload_to='')
    feedback_job = models.ForeignKey('FeedbackJob', verbose_name='Заявка', on_delete=models.CASCADE, related_name='feedback_job_photo', null=True, blank=True)

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотография'
