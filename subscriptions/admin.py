from django.contrib import admin
from django.contrib.admin import ModelAdmin, StackedInline, register
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

from .models import Account, Author, Book

admin.site.unregister(User)


class AccountInline(StackedInline):
    model = Account
    can_delete = False


@register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (
        AccountInline,
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
