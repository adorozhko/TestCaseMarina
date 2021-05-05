from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer

from .models import Account, Author, Book


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}


class AccountSerializer(ModelSerializer):
    user = UserSerializer()

    def create(self, validated_data):
        user = validated_data.get('user', None)
        if not user:
            raise ValueError('user not found')

        if not user.get('username'):
            raise ValueError('username not found')

        if not user.get('password'):
            raise ValueError('password not found')

        subscription = validated_data.get('subscription', None)
        if not subscription:
            raise ValueError('subscription not found')

        user = User.objects.create_user(**user)
        reader = Account.objects.create(user=user, subscription=subscription)
        return reader

    class Meta:
        model = Account
        fields = '__all__'


class AuthorSerializer(ModelSerializer):
    class Meta:
        model = Author
        fields = '__all__'


class BookSerializer(ModelSerializer):
    class Meta:
        model = Book
