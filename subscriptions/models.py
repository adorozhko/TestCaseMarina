from datetime import date, timedelta

from django.db.models import (PROTECT, CharField, DateField, ForeignKey,
                              ManyToManyField, Model, TextChoices, TextField)
from django.utils.translation import gettext_lazy as _


class User(Model):
    name = CharField(max_length=50)
    subscription = DateField(
        default=date.today() + timedelta(weeks=2)
    )

    def __str__(self):
        return self.name

    def is_active(self):
        return self.subscription >= date.today()

    def update_subscription(self, days):
        self.subscription += timedelta(days=days)
        self.save()
        return self.subscription


class Author(Model):
    name = CharField(max_length=50)
    surname = CharField(max_length=50)
    about = TextField(blank=True)
    books = ManyToManyField(
        'Book',
        through='AuthorBook',
        blank=True
    )

    def __str__(self):
        return self.name


class Book(Model):
    class Type(TextChoices):
        TEXT = 'TXT', _('Text')
        AUDIO = 'AUDIO', _('Audio')

    class Genre(TextChoices):
        COMEDY = 'COMEDY', _('Comedy')
        TRAGEDY = 'TRAGEDY', _('Tragedy')
        DRAMA = 'DRAMA', _('Drama')
        HORROR = 'HORROR', _('Horror')

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
