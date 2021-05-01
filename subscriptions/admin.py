from django.contrib.admin import ModelAdmin, register

from .models import Author, Book, User


@register(User)
class UserAdmin(ModelAdmin):
    list_display = (
        'name',
        'subscription'
    )


@register(Author)
class AuthorAdmin(ModelAdmin):
    list_display = (
        'name',
        'surname',
        'about'
    )
    filter_horizontal = (
        'books',
    )


@register(Book)
class BookAdmin(ModelAdmin):
    list_display = (
        'title',
        'type',
        'genre'
    )
    filter_horizontal = (
        'authors',
    )
