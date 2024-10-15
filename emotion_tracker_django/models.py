import uuid
from django.db import models

class Day(models.Model):
    # Explicitly specify the table name
    class Meta:
        db_table = 'days'

    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name="days")
    date = models.DateField(unique=True)

    #todo: temp: Override the save method to set a default user
    def save(self, *args, **kwargs):
        # If no user is set, default to User.first()
        if not self.user_id:
            self.user = User.objects.first()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Day {self.date} for {self.user.email}'



class DayPeriod(models.Model):
    # Explicitly specify the table name
    class Meta:
        db_table = 'day_periods'

    day = models.ForeignKey('Day', on_delete=models.CASCADE, related_name='day_periods')
    period = models.ForeignKey('Period', on_delete=models.CASCADE, related_name='day_periods')
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='day_periods')

    #todo: temp: Override the save method to set a default user
    def save(self, *args, **kwargs):
        # If no user is set, default to User.first()
        if not self.user_id:
            self.user = User.objects.first()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.day.date} - {self.period.name} for {self.user.email}'


class Period(models.Model):
    class Meta:
        db_table = 'periods'

    name = models.CharField(max_length=255, unique=True)
    days = models.ManyToManyField('Day', through='DayPeriod')

    def __str__(self):
        return self.name


class Emotion(models.Model):
    class Meta:
        db_table = 'emotions'

    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Entry(models.Model):
    class Meta:
        db_table = 'entries'

    day_period = models.ForeignKey('DayPeriod', on_delete=models.CASCADE, related_name='entries')
    emotion = models.ForeignKey('Emotion', on_delete=models.CASCADE, related_name='entries')
    # todo: convert to uuid field here, and to actual uuid type in db
    uuid = models.CharField(default=uuid.uuid4, max_length=36, editable=False, unique=True)
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='entries')

    #todo: temp: Override the save method to set a default user
    def save(self, *args, **kwargs):
        # If no user is set, default to User.first()
        if not self.user_id:
            self.user = User.objects.first()
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Entry {self.uuid} for Day Period {self.day_period.id} and Emotion {self.emotion.name}'


class User(models.Model):
    class Meta:
        db_table = 'users'

    email = models.EmailField(unique=True)
    encrypted_password = models.CharField(max_length=255)
    reset_password_token = models.CharField(max_length=255, blank=True, null=True)
    reset_password_sent_at = models.DateTimeField(blank=True, null=True)
    remember_created_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email