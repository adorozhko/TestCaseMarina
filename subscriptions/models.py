from datetime import date, timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.db.models import (CASCADE, PROTECT, BigAutoField, CharField,
                              DateField, ForeignKey, ManyToManyField, Model,
                              OneToOneField, TextChoices, TextField)
from django.utils.translation import gettext_lazy as _


class Account(Model):
    user = OneToOneField(User, on_delete=CASCADE)
    subscription = DateField()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if not self.pk:
            if self.subscription < date.today():
                self.subscription = date.today()
            self.subscription += timedelta(days=settings.DEFAULT_TRIAL_PERIOD)
        super().save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return self.user.get_full_name()

    def is_active(self):
        return self.subscription >= date.today()

    def update_subscription(self, days):
        if self.subscription < date.today():
            self.subscription = date.today()

        self.subscription += timedelta(days=days)
        self.save()
        return self.subscription


class Author(Model):
    id = BigAutoField(primary_key=True)
    name = CharField(max_length=50)
    surname = CharField(max_length=50)
    about = TextField(blank=True)
    books = ManyToManyField(
        'Book',
        through='AuthorBook',
        blank=True
    )

    def __str__(self):
        return f'{self.name} {self.surname}'


class Book(Model):
    class Type(TextChoices):
        TEXT = 'TEXT', _('Text')
        AUDIO = 'AUDIO', _('Audio')

    class Genre(TextChoices):
        COMEDY = 'COMEDY', _('Comedy')
        TRAGEDY = 'TRAGEDY', _('Tragedy')
        DRAMA = 'DRAMA', _('Drama')
        HORROR = 'HORROR', _('Horror')

    id = BigAutoField(primary_key=True)
    title = CharField(max_length=50)
    type = CharField(
        max_length=50,
        choices=Type.choices,
        default=Type.TEXT
    )
    genre = CharField(
        max_length=50,
        choices=Genre.choices,
        default=Genre.DRAMA
    )
    about = TextField(blank=True)
    authors = ManyToManyField(
        'Author',
        through='AuthorBook',
        blank=True
    )

    def __str__(self):
        return self.title


class AuthorBook(Model):
    author = ForeignKey(Author, on_delete=PROTECT)
    book = ForeignKey(Book, on_delete=PROTECT)

    class Meta:
        auto_created = True
