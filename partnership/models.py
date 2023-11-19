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
    """Контакты и настройки"""
    fio = models.CharField(verbose_name='ФИО', max_length=200)
    phone = models.CharField(verbose_name='Мобильный телефон', max_length=20, validators=[phone_validator])
    time_start = models.CharField(verbose_name='Время начала работы', max_length=7)
    time_end = models.CharField(verbose_name='Время окончания работы', max_length=7)
    feedback_limit = models.IntegerField(verbose_name='Число заявок в день', default=2)
    map = models.TextField(verbose_name='ссылка на яндекс карту', help_text='Вставить ссылку с: https://yandex.ru/map-constructor (выбирать width="600%" height="400")')
    address = models.TextField(verbose_name='Адрес')

    class Meta:
        verbose_name = 'Контакты и настройки'
        verbose_name_plural = 'Контакты и настройки'

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
    apartment = models.IntegerField(verbose_name='Квартира', validators=[MinValueValidator(1), MaxValueValidator(550)])
    entrance = models.IntegerField(verbose_name='Подъезд', validators=[MinValueValidator(1), MaxValueValidator(9)])
    phone = models.CharField(verbose_name='Телефон', max_length=20, validators=[phone_validator])
    message = models.TextField(verbose_name='Сообщение')
    status = models.CharField(verbose_name='Статус', max_length=10, choices=STATUS_CHOICES, default='-')
    datetime_start = models.DateTimeField(verbose_name='Дата заявки', auto_now_add=True)
    datetime_end = models.DateField(verbose_name='Дата закрытия заявки', null=True, blank=True)
    message_comment = models.TextField(verbose_name='Ответ от председателя', null=True, blank=True)

    class Meta:
        verbose_name = 'Заявки'
        verbose_name_plural = 'Заявки'
        ordering = '-datetime_start',

    def fio_phone(self):
        return f'{self.last_name} {self.first_name} {self.middle_name} ({self.phone})'

    fio_phone.short_description = 'ФИО (телефон)'

    def __str__(self):
        return f'{self.last_name} {self.first_name} {self.middle_name}'

    def save(self, *args, **kwargs):
        if self.status == 'Выполнен' and not self.datetime_end:
            self.datetime_end = timezone.now().date()
        elif self.status != 'Выполнен':
            self.datetime_end = None  # Сбрасываем дату, если статус не "Выполнен"
        super().save(*args, **kwargs)

    def photo_count(self):
        return f'{self.feedback_job_photo.count()} шт.'

    photo_count.short_description = 'Фотографии'


class Photo(models.Model):
    """Фотография"""
    photo = models.ImageField(verbose_name='Фотография', upload_to='')
    feedback_job = models.ForeignKey('FeedbackJob', verbose_name='Заявка', on_delete=models.CASCADE, related_name='feedback_job_photo', null=True, blank=True)

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотография'

    def __str__(self):
        return f'{self.id} - {self.feedback_job.id}'


class UserInfo(models.Model):
    """Информация о жильцах"""
    fio = models.CharField(verbose_name='Фамилия', max_length=100, null=True, blank=True)
    phone = models.CharField(verbose_name='Телефон', max_length=20, null=True, blank=True)
    apartment = models.CharField(verbose_name='Квартира', max_length=3, null=True, blank=True)
    entrance = models.CharField(verbose_name='Подъезд', max_length=1, null=True, blank=True)
    ip = models.CharField(verbose_name='ip', max_length=200, null=True, blank=True)
    user_agent = models.TextField(verbose_name='Пользовательский агент', null=True, blank=True)
    datetime_add = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)
    country_info = models.TextField(verbose_name='Дополнительная информация', null=True, blank=True)

    class Meta:
        verbose_name = 'Информация о жильцах'
        verbose_name_plural = 'Информация о жильцах'

    def __str__(self):
        return self.fio

    def fio_phone(self):
        return f'{self.fio} ({self.phone})'

    fio_phone.short_description = 'ФИО (телефон)'
