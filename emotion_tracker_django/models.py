import uuid
from django.db import models

class Day(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="days")
    date = models.DateField(unique=True)

    # Explicitly specify the table name
    class Meta:
        db_table = 'days'

    def __str__(self):
        return f'Day {self.date} for {self.user.email}'


class DayPeriod(models.Model):
    day = models.ForeignKey('Day', on_delete=models.CASCADE, related_name='day_periods')
    period = models.ForeignKey('Period', on_delete=models.CASCADE, related_name='day_periods')
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='day_periods')

    # Explicitly specify the table name
    class Meta:
        db_table = 'day_periods'

    def __str__(self):
        return f'{self.day.date} - {self.period.name} for {self.user.email}'


class Period(models.Model):
    name = models.CharField(max_length=255, unique=True)
    days = models.ManyToManyField('Day', through='DayPeriod')

    class Meta:
        db_table = 'periods'

    def __str__(self):
        return self.name


class Emotion(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = 'emotions'

    def __str__(self):
        return self.name


class Entry(models.Model):
    day_period = models.ForeignKey('DayPeriod', on_delete=models.CASCADE, related_name='entries')
    emotion = models.ForeignKey('Emotion', on_delete=models.CASCADE, related_name='entries')
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='entries')

    class Meta:
        db_table = 'entries'

    def __str__(self):
        return f'Entry {self.uuid} for Day Period {self.day_period.id} and Emotion {self.emotion.name}'


class User(models.Model):
    email = models.EmailField(unique=True)
    encrypted_password = models.CharField(max_length=255)
    reset_password_token = models.CharField(max_length=255, blank=True, null=True)
    reset_password_sent_at = models.DateTimeField(blank=True, null=True)
    remember_created_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.email